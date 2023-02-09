package com.example.aventurasdemarcoyluis.model.characters.interfaces;

import com.example.aventurasdemarcoyluis.model.game.patterns.visitors.CharacterVisitor;

/***
 * General interface for all characters
 */
public interface Character {
    int getAtk();
    int getLvl();
    int getDef();
    void minusHp(int amount);
    void acceptGeneral(CharacterVisitor visitor);
    public int generateRandomInt(int min, int max);
}
