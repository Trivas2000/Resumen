package com.example.aventurasdemarcoyluis.model.game.patterns.visitors;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;


/***
 * Father class for implementing the visitor pattern design, it can be accepted by enemies or lists of enemies
 */
public class EnemiesVisitor {

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
}
