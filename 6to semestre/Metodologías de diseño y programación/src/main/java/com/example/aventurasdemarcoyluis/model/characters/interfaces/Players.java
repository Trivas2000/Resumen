package com.example.aventurasdemarcoyluis.model.characters.interfaces;

import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;
import com.example.aventurasdemarcoyluis.model.items.Arsenal;

/***
 * General interface for all players
 */
public interface Players extends Character{
    void addFp(int i);

    int getHp();

    int getMaxHp();

    int getAtk();

    int getLvl();

    int getDef();

    int getFp();

    void setHp(int i);

    void getsAttackedByGoomba(Goomba enemy);

    void getsAttackedBySpiny(Spiny spiny);

    void setItems(Arsenal arsenal);

    int itemAmount(String item);

    boolean isKod();

    int generateRandomInt(int min, int max);

    void setSeed(long seed);
}
