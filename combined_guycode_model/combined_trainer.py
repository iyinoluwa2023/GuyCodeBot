from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU
from aitextgen import aitextgen

model_parent = "/Users/iyinoluwatugbobo/Desktop/Development/guyCodeAI/combined_guycode_model"
model_dir = "/Users/iyinoluwatugbobo/Desktop/Development/guyCodeAI/combined_guycode_model/trained_model"
input_file = "/Users/iyinoluwatugbobo/Desktop/Development/guyCodeAI/combined_guycode_model/combined_input.txt"

train_tokenizer(input_file)
tokenizer_file = "aitextgen.tokenizer.json"
config = GPT2ConfigCPU()

def train():
    ai = aitextgen(tokenizer_file=tokenizer_file, config=config)
    data = TokenDataset(input_file, tokenizer_file=tokenizer_file, block_size=64)
    ai.train(data,
             batch_size=8,
             num_steps=50000,
             generate_every=10000,
             save_every=10000,
             output_dir=model_dir)

train()