package com.example.aventurasdemarcoyluis.model.items;

import com.example.aventurasdemarcoyluis.model.characters.interfaces.Players;
import com.example.aventurasdemarcoyluis.model.items.AbstractClasses.Item;

/***
 * An item that heals 10% of the players max Hp
 */
public class RedMushroom extends Item {
    public RedMushroom() {
        super("Red Mushroom");
    }

    /***
     * Heals the player by 10% of maxHp
     * @param player the player that is using the item
     */
    @Override
    public void useItem(Players player) {player.setHp(player.getHp() + player.getMaxHp() / 10);}
}
