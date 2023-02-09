package com.example.aventurasdemarcoyluis.model.game.patterns.visitors;

import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;
import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;
/***
 * Visitor that checks if a character is a luis
 */
public class CheckIfLuisVisitor extends CharacterVisitor{
    private boolean result=false;

    /***
     * Returns false because goomba is not luis
     * @param goomba Goomba the visitor visits
     */
    @Override
    public void visitGoomba(Goomba goomba) {result=false;
    }

    /***
     * Returns false because spiny is not luis
     * @param spiny Spiny the visitor visits
     */
    @Override
    public void visitSpiny(Spiny spiny) {result=false;

    }

    /***
     * Returns false because boo is not luis
     * @param boo Boo the visitor visits
     */
    @Override
    public void visitBoo(Boo boo) {result=false;

    }

    /***
     * Returns false because marco is not luis
     * @param marco Marco the visitor visits
     */
    @Override
    public void visitMarco(Marco marco) {result=false;
    }

    /***
     * Returns true because luis is luis
     * @param luis Luis the visitor visits
     */
    @Override
    public void visitLuis(Luis luis) {result=true;

    }

    /***
     * Getter for result
     * @return the result
     */
    public boolean getResult() {return result;}
}
