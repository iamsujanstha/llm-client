
def calculate_budget(
    context_window: int,
    max_output_tokens: int,
    safety_margin: int = 256,
):
    input_budget = (
        context_window
        - max_output_tokens
        - safety_margin
    )

    if input_budget <= 0:
        raise ValueError("Invalid token budget configuration")

    return input_budget


if __name__ == "__main__":
    budget = calculate_budget(
        context_window=8192,
        max_output_tokens=1500,
        safety_margin=692,
    )

    print("Available input budget:", budget)
