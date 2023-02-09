package com.example.aventurasdemarcoyluis.model.characters.players;

import com.example.aventurasdemarcoyluis.model.characters.AbstractClasses.AbstractPlayers;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.Character;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.Enemies;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.HammerAttackedByMarco;
import com.example.aventurasdemarcoyluis.model.game.patterns.visitors.CharacterVisitor;

/***
 * Luis brother and one of the main characters. Is famous mainly for being Luis's older brother
 */
public class Marco extends AbstractPlayers implements Character {
    /**
     * The name is Marco by default
     * @param ATK Amount of attack points
     * @param DEF Amount of defense points
     * @param maxHp amount of hit points
     * @param LVL Current character level
     */
    public Marco(int ATK, int DEF, int maxHp, int maximumFp, int LVL) {
        super(ATK,DEF,maxHp,maximumFp,LVL,"Marco");}

    /***
     * Simulates Marco attacking the enemy with a jump attack
     * @param enemy the enemy Luis is attacking
     */
    public void jumpAttacks(Enemies enemy) {
        if(!isKod() && getFp()>0){
            enemy.getsJumpAttackedByMarco(this);
            this.addFp(-1);}}

    /***
     * Simulates Marco attacking the enemy with a hammer attack
     * @param enemy the enemy Luis is attacking
     */
    public void hammerAttacks(HammerAttackedByMarco enemy) {
        if(!this.isKod() && getFp()>1){
            enemy.getsHammerAttackedByMarco(this);
            this.addFp(-2);}}

    /***
     * Simulates Marco getting attacked by a goomba
     * @param goomba the attacker
     */
    @Override
    public void getsAttackedByGoomba(Goomba goomba) {getStandardAttacked(goomba);}

    /***
     * Simulates Marco getting attacked by a spiny
     * @param spiny the attacker
     */
    @Override
    public void getsAttackedBySpiny(Spiny spiny) {getStandardAttacked(spiny);}


    /***
     * The marco accepts a visitor
     * @param visitor the visitor to accept
     */
    @Override
    public void acceptGeneral(CharacterVisitor visitor) {visitor.visitMarco(this);
    }
}
