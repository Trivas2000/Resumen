package com.example.aventurasdemarcoyluis.model.game.patterns.visitors;

import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;

/***
 * Visitor that checks if an enemy is hammer attackable
 */
public class HammerAttackableVisitor extends EnemiesVisitor{
    private boolean result=false;
    /***
     * Returns true because goomba can be hammer attacked
     * @param goomba Goomba the visitor visits
     */
    public void visitGoomba(Goomba goomba) {result = true;
    }

    /***
     * Returns true because spiny can be hammer attacked
     * @param spiny Spiny the visitor visits
     */
    public void visitSpiny(Spiny spiny) {result = true;
    }

    /***
     * Returns false because boo can not be hammer attacked
     * @param boo Boo the visitor visits
     */
    public void visitBoo(Boo boo) {result = false;
    }

    /***
     * Getter for result
     * @return the current result of the visitor
     */
    public boolean getResult() {return result;
    }

}
