package com.example.aventurasdemarcoyluis.model.game.patterns.visitors;

import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;
import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;

/***
 * Father class for implementing the visitor pattern design, it can be accepted by any character
 */
public class CharacterVisitor {

    /***
     * Empty method
     * @param goomba Goomba the visitor visits
     */
    public void visitGoomba(Goomba goomba) {

    }

    /***
     * Empty method
     * @param spiny Spiny the visitor visits
     */
    public void visitSpiny(Spiny spiny) {

    }

    /***
     * Empty method
     * @param boo Boo the visitor visits
     */
    public void visitBoo(Boo boo) {

    }

    /***
     * Empty method
     * @param marco Marco the visitor visits
     */
    public void visitMarco(Marco marco) {

    }

    /***
     * Empty method
     * @param luis Marco the visitor visits
     */
    public void visitLuis(Luis luis) {

    }
}
