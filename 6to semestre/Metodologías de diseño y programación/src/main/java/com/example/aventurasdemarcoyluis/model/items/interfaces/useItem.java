package com.example.aventurasdemarcoyluis.model.items.interfaces;

import com.example.aventurasdemarcoyluis.model.characters.interfaces.Players;

/***
 * An interface for all items that have a use on the character
 */
public interface useItem {
    void useItem(Players player);
    String getName();
    int getAmount();
    void add(int newAmount);
}
