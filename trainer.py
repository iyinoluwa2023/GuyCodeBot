from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU
from aitextgen import aitextgen

tokenizer_file = "aitextgen.tokenizer.json"
config = GPT2ConfigCPU()

def train(user):
    user = user.strip("\n")
    file_name = f"user_data/{user}.txt"
    # print(file_name)
    train_tokenizer(file_name)
    ai = aitextgen(tokenizer_file=tokenizer_file, config=config)
    data = TokenDataset(file_name, tokenizer_file=tokenizer_file, block_size=64)
    print(f"======================== {user} ========================")
    ai.train(data,
             batch_size=8,
             num_steps=20000,
             learning_rate=1e-5,
             output_dir=f"user_data/{user}/trained_model")

def generate(prompt):
    ai2 = aitextgen(model_folder="trained_model",
                    tokenizer_file="aitextgen.tokenizer.json")
    ai2.generate(10, prompt=prompt)

def training_session():
    with open("guycode.txt") as f:
        for user in f:
            train(user)
        f.close()

training_session()