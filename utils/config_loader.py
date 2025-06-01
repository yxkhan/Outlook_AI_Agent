import yaml

def load_config(config_path: str = r"C:\Users\Yaseen Khan\Documents\Data Sceince\Hackathon\Infy_Hackathon\config\config.yaml") -> dict:
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config