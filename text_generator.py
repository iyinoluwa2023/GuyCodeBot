from aitextgen import aitextgen

def generate_all(prompt=""):
    with open("guycode.txt") as file:
        for user in file:
            user_folder = "user_data/" + user.strip('\n') + "/trained_model"
            print(user_folder)
            text_gen = aitextgen(model_folder=user_folder,
                                 tokenizer_file="aitextgen.tokenizer.json")
            text_gen.generate(10, prompt=prompt)
        file.close()


# text_gen = aitextgen(model_folder="user_data/kaineagain/trained_model",
#                      tokenizer_file="aitextgen.tokenizer.json")
# text_gen.generate(10)
generate_all()