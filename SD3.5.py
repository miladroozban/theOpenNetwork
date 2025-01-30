import hashlib
from huggingface_hub import InferenceClient
from datetime import datetime
client = InferenceClient(
	provider="hf-inference",
	api_key="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"
)
#convert to sha256
def convert_sha(number):
    number_str = str(number)
    number_bytes = number_str.encode('utf-8')
    hasher = hashlib.sha256()
    hasher.update(number_bytes)
    sha256_hash = hasher.hexdigest()
    return sha256_hash


images_path =input("Enter the path of images folder: ")
images_path.replace("\n", "\\")
images_format=".jpg"

while images_path:
	exit_key = "e"
	if images_path == exit_key:
		break
	prompt= input("Enter your Prompt: ")
	if prompt == exit_key:
		break

	if prompt:
		save_file = images_path + convert_sha(datetime.now().strftime("%H-%M-%S-") + prompt[0:5]) + images_format
		image = client.text_to_image(
			prompt,
			model="stabilityai/stable-diffusion-3.5-large"
		)
		image.save(save_file)
		print(f"Image saved to : {save_file}")
		image.show()






