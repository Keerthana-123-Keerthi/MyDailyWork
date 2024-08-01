import java.time.LocalTime;
import java.util.*;

public class chatbot {

    public static String getResponse(String userInput) {
        userInput = userInput.toLowerCase(); // Convert input to lowercase for case-insensitive matching
        
        if (userInput.contains("hello") || userInput.contains("hi")) {
            return "Hello! How can I help you today?";
        } else if (userInput.contains("how are you")) {
            return "I'm just a chatbot, but I'm here to help you!";
        } else if (userInput.contains("what is your name")) {
            return "I don't have a name, but you can call me Chatbot.";
        } else if (userInput.contains("bye")) {
            return "Goodbye! Have a great day!";
        } else if (userInput.contains("what is your favorite color")) {
            return "I don't have personal preferences, but I hear blue is a popular color!";
        } else if (userInput.contains("what is the time now")) {
            return "The current time is " + LocalTime.now().withNano(0).toString() + ".";
        }else {
            return "Sorry, I don't understand that. Can you ask something else?";
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Chatbot: Hi there! Type 'bye' to end the conversation.");

        while (true) {
            System.out.print("You: ");
            String userInput = scanner.nextLine();
            String response = getResponse(userInput);
            System.out.println("Chatbot: " + response);
            if (userInput.toLowerCase().contains("bye")) {
                break;
            }
        }

        scanner.close();
    }
}
