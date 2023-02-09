package com.example.aventurasdemarcoyluis.model.items;

import com.example.aventurasdemarcoyluis.model.characters.interfaces.Players;
import com.example.aventurasdemarcoyluis.model.items.AbstractClasses.Item;

/***
 * An item that adds 3 fp to the player
 */
public class HoneySyrup extends Item {
    public HoneySyrup() {
        super("Honey Syrup");
    }

    /***
     * Adds 3 Fp to te player
     * @param player the player that is using the item
     */
    @Override
    public void useItem(Players player) {player.addFp(3);}
}
