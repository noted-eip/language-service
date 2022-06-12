import os

def get_required_env_variable(name: str) -> str:
    result = os.getenv(name);
    if result is None:
        raise EnvironmentError(f"Please set the {name} env variable")
    return result
