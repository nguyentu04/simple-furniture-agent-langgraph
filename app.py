from graph import build_graph


def main():
    graph = build_graph()

    print("Simple Furniture Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("User: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        state = {
            "user_input": user_input,
            "intent": None,
            "tool_result": None,
            "final_response": None,
        }

        result = graph.invoke(state)

        print("Agent:", result["final_response"])
        print()


if __name__ == "__main__":
    main()