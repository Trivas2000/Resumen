package com.example.aventurasdemarcoyluis.model.characters.interfaces;

import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;
import com.example.aventurasdemarcoyluis.model.game.patterns.visitors.EnemiesVisitor;

/***
 * general interface for all enemies
 */
public interface Enemies extends Character{
    void getsJumpAttackedByMarco(Marco attacker);

    int getLvl();

    int getAtk();

    int getHp();

    int getDef();

    boolean isKod();

    void setHp(int Hp);

    void accept(EnemiesVisitor enemiesVisitor);

    void setSeed(long seed);
}
