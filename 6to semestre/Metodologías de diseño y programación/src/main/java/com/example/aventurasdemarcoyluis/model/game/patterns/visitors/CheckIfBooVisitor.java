package com.example.aventurasdemarcoyluis.model.game.patterns.visitors;

import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;
import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;

/***
 * Visitor that checks if a character is a boo
 */
public class CheckIfBooVisitor extends CharacterVisitor{
    private boolean result=false;

    /***
     * Returns false because goomba is not boo
     * @param goomba Goomba the visitor visits
     */
    @Override
    public void visitGoomba(Goomba goomba) {result=false;
    }

    /***
     * Returns false because spiny is not boo
     * @param spiny Spiny the visitor visits
     */
    @Override
    public void visitSpiny(Spiny spiny) {result=false;

    }

    /***
     * Returns true because boo is a boo
     * @param boo Boo the visitor visits
     */
    @Override
    public void visitBoo(Boo boo) {result=true;

    }

    /***
     * Returns false because marco is not a boo
     * @param marco Marco the visitor visits
     */
    @Override
    public void visitMarco(Marco marco) {result=false;

    }

    /***
     * Returns false because luis
     * @param luis Luis the visitor visits
     */
    @Override
    public void visitLuis(Luis luis) {result=false;

    }

    /***
     * Getter for result
     * @return the result
     */
    public boolean getResult() {return result;}
}