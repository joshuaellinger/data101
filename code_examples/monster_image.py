import requests

def generate_monster_image(monster_name: str):

    # this code will not work until sign up and get an API key.
    
    # to simulate,
    #    1. go to https://deepai.org/machine-learning-model/fantasy-character-generator
    #    2. type in '<monster name> monster'.  Adding the extra word monster makes it
    #    look a lot more like a monster
    #    3. save the image to a file
    #    4. copy it to the images folder
    #
    r = requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            'text': monster_name + " monster",
        },
        headers={'api-key': 'YOUR_API_KEY'}
    )
    print(r.json())

    #todo: save the image to a file

generate_monster_image("Giant Ant")
