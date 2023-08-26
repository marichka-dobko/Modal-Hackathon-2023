import os
import modal
from modal import Image, Secret, Stub, method
import huggingface_hub

MODEL_DIR = "/model"


def download_model_to_folder():
    from huggingface_hub import snapshot_download

    snapshot_download(
        "meta-llama/Llama-2-13b-chat-hf",
        local_dir="/model",
        token=os.environ['HUGGINGFACE_TOKEN'],
    )

image = (
    Image.from_registry("nvcr.io/nvidia/pytorch:22.12-py3")
    .pip_install(
        "torch==2.0.1", index_url="https://download.pytorch.org/whl/cu118"
    )
    # Pinned to 08/15/2023
    .pip_install(
        "vllm @ git+https://github.com/vllm-project/vllm.git@805de738f618f8b47ab0d450423d23db1e636fa2",
        "typing-extensions==4.5.0",  # >=4.6 causes typing issues
    )
    # Use the barebones hf-transfer package for maximum download speeds. No progress bar, but expect 700MB/s.
    .pip_install("hf-transfer~=0.1")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .run_function(
        download_model_to_folder,
        secret=Secret.from_name("my-huggingface-secret"),
        timeout=60 * 20,
    )
)

stub = Stub("example-vllm-inference", image=image)


# ## The model class
#
# The inference function is best represented with Modal's [class syntax](/docs/guide/lifecycle-functions) and the `__enter__` method.
# This enables us to load the model into memory just once every time a container starts up, and keep it cached
# on the GPU for each subsequent invocation of the function.
#
# The `vLLM` library allows the code to remain quite clean.
@stub.cls(gpu="A100", secret=Secret.from_name("my-huggingface-secret"))
class Model:
    def __enter__(self):
        from vllm import LLM

        # Load the model. Tip: MPT models may require `trust_remote_code=true`.
        self.llm = LLM(MODEL_DIR)
        self.template = """<s>[INST] <<SYS>>
        {system}
        <</SYS>>

        {user} [/INST] """

    @method()
    def generate(self, user_questions):
        from vllm import SamplingParams

        prompts = [
            self.template.format(system="", user=q) for q in user_questions
        ]
        sampling_params = SamplingParams(
            temperature=0.75,
            top_p=1,
            max_tokens=800,
            presence_penalty=1.15,
        )
        result = self.llm.generate(prompts, sampling_params)
        num_tokens = 0
        for output in result:
            num_tokens += len(output.outputs[0].token_ids)
            print(output.prompt, output.outputs[0].text, "\n\n", sep="")
        print(f"Generated {num_tokens} tokens")


# ## Run the model
# We define a [`local_entrypoint`](/docs/guide/apps#entrypoints-for-ephemeral-apps) to call our remote function
# sequentially for a list of inputs. You can run this locally with `modal run vllm_inference.py`.

@stub.local_entrypoint()
def main():
    model = Model()
    user_input = ''
    general_prompt = "From this list, rank them according to most important to least important for a patient: {}" \
    "Price Per Month, Metal Tier (Bronze, Silver, Gold, Platinum), Overall Quality Rating, Maximum Out-of-Pocket Expense," \
    " Out-of-Network Coverage, Health Savings Account (HSA) Eligibility, Persons Covered (Individual, Family, Group), Deductible Amount," \
    "Co-payments for Services, Prescription Drug Coverage, Emergency Services Coverage, Network of Doctors/Hospitals," \
    "Preventive Services, Mental Health Services, Maternity and Newborn Care, Duration of Coverage, Waiting Period, " \
    "Exclusions and Limitations, Renewability, Telehealth Options, Customer Service Quality, Additional Benefits (e.g., Dental, Vision)," \
    "Claim Settlement Ratio, Portability Options, Policy Cancellation Terms"

    res = model.generate.remote([general_prompt.replace('{}', user_input)])

    print(res)
