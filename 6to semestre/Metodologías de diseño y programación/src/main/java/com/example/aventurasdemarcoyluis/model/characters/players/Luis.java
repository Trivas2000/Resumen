package com.example.aventurasdemarcoyluis.model.characters.players;

import com.example.aventurasdemarcoyluis.model.characters.AbstractClasses.AbstractPlayers;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.AttackedByBoo;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.Character;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.JumpedAttackedByLuis;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.HammerAttackedByLuis;
import com.example.aventurasdemarcoyluis.model.game.patterns.visitors.CharacterVisitor;


/***
 * One of our main characters and Marcos brother. He wears a green overall and is a bit taller than Marcos.
 */
public class Luis extends AbstractPlayers implements AttackedByBoo, Character {
    /**
     * The name is Luis by default
     * @param ATK Amount of attack points
     * @param DEF Amount of defense points
     * @param maxHp amount of hit points
     * @param LVL Current character level
     */
    public Luis(int ATK, int DEF, int maxHp, int maximumFp, int LVL) {
        super(ATK, DEF, maxHp, maximumFp, LVL, "Luis");
    }

    /***
     * Simulates Luis attacking the enemy with a jump attack
     * @param enemy the enemy Luis is attacking
     */
    public void jumpAttacks(JumpedAttackedByLuis enemy) {
        if(!isKod() && getFp()>0){
            enemy.getsJumpAttackedByLuis(this);
            this.addFp(-1);}}


    /***
     * Simulates Luis attacking the enemy with a hammer attack
     * @param enemy the enemy Luis is attacking
     */

    public void hammerAttacks(HammerAttackedByLuis enemy) {
        if(!this.isKod() && getFp()>1){
            enemy.getsHammerAttackedByLuis(this);
            this.addFp(-2);}}

    /***
     * Simulates Luis getting attacked by a goomba
     * @param goomba the attacker
     */

    @Override
    public void getsAttackedByGoomba(Goomba goomba) {getStandardAttacked(goomba);}

    /***
     * Simulates Luis getting attacked by a spiny
     * @param spiny the attacker
     */
    @Override
    public void getsAttackedBySpiny(Spiny spiny) {getStandardAttacked(spiny);}

    /***
     * Simulates Luis getting attacked by a boo
     * @param boo the attacker
     */
    public void getsAttackedByBoo(Boo boo) {getStandardAttacked(boo);}


    /***
     * The luis accepts a visitor
     * @param visitor the visitor to accept
     */
    @Override
    public void acceptGeneral(CharacterVisitor visitor) {visitor.visitLuis(this);
    }
}
