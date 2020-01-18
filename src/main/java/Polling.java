import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

public class Polling extends TelegramLongPollingBot {

    private static String DADDY_DANNY = "Daddy Danny";
    private static String TOKEN = "1016477578:AAGmmknBxRKyIbh_2XmRhcuK-fXwW0wJ9JE";

    @Override
    public void onUpdateReceived(Update update) {
        if (update.hasMessage() && update.getMessage().hasText()) {
            SendMessage message = new SendMessage() // Create a SendMessage object with mandatory fields
                    .setChatId(update.getMessage().getChatId())
                    .setText(update.getMessage().getText());
            try {
                execute(message); // Call method to send the message
            } catch (TelegramApiException e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    public String getBotUsername() {
        return DADDY_DANNY;
    }

    @Override
    public String getBotToken() {
        return TOKEN;
    }

}
