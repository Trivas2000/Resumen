module com.example.aventurasdemarcoyluis {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.aventurasdemarcoyluis to javafx.fxml;
    exports com.example.aventurasdemarcoyluis;
    opens com.example.aventurasdemarcoyluis.model to javafx.fxml;
    exports com.example.aventurasdemarcoyluis.model.items;
    opens com.example.aventurasdemarcoyluis.model.items to javafx.fxml;
    opens com.example.aventurasdemarcoyluis.model.characters to javafx.fxml;
    exports com.example.aventurasdemarcoyluis.model.characters.enemies;
    opens com.example.aventurasdemarcoyluis.model.characters.enemies to javafx.fxml;
    exports com.example.aventurasdemarcoyluis.model.characters.players;
    opens com.example.aventurasdemarcoyluis.model.characters.players to javafx.fxml;
    exports com.example.aventurasdemarcoyluis.model.characters.AbstractClasses;
    opens com.example.aventurasdemarcoyluis.model.characters.AbstractClasses to javafx.fxml;
    exports com.example.aventurasdemarcoyluis.model.characters.interfaces;
    opens com.example.aventurasdemarcoyluis.model.characters.interfaces to javafx.fxml;
    exports com.example.aventurasdemarcoyluis.model.items.AbstractClasses;
    opens com.example.aventurasdemarcoyluis.model.items.AbstractClasses to javafx.fxml;
    exports com.example.aventurasdemarcoyluis.model.items.interfaces;
    opens com.example.aventurasdemarcoyluis.model.items.interfaces to javafx.fxml;
}