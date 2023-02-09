package com.example.aventurasdemarcoyluis.model.game.patterns.visitors;

import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;
import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;

/***
 * Visitor that checks if a character is a player
 */
public class CheckIfPlayerVisitor extends CharacterVisitor{
    private boolean result=false;

    /***
     * Returns false because goomba is not a player
     * @param goomba Goomba the visitor visits
     */
    @Override
    public void visitGoomba(Goomba goomba) {result=false;
    }

    /***
     * Returns false because spiny is not a player
     * @param spiny Spiny the visitor visits
     */
    @Override
    public void visitSpiny(Spiny spiny) {result=false;

    }

    /***
     * Returns false because boo is not a player
     * @param boo Boo the visitor visits
     */
    @Override
    public void visitBoo(Boo boo) {result=false;

    }
    /***
     * Returns true because marco is a player
     * @param  marco Marco the visitor visits
     */
    @Override
    public void visitMarco(Marco marco) {result=true;

    }

    /***
     * Returns true because luis is a player
     * @param  luis Luis the visitor visits
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
