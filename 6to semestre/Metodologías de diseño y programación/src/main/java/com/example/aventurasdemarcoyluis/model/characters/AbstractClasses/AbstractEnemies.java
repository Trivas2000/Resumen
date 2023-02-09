package com.example.aventurasdemarcoyluis.model.characters.AbstractClasses;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.Enemies;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.Players;

/***
 * This class represents the common ground for all the enemies in the game
 */

public abstract class AbstractEnemies extends AbstractCharacter implements Enemies {
    /***
     * @param ATK Amount of attack points
     * @param DEF Amount of defense points
     * @param MaxHp amount of hit points
     * @param LVL Current character level
     * @param enemyType The string that represents the enemy name
     */
    public AbstractEnemies(int ATK, int DEF, int MaxHp, int LVL, String enemyType) {
        super(ATK, DEF, MaxHp, LVL, enemyType);
    }

    /***
     * @param attacker the attacking character
     * This function models the standard interaction of a jump attack on the enemy
     */
    protected void getStandardJumpedAttacked(Players attacker) {minusHp(calculateDmg(1, attacker.getAtk(), def, attacker.getLvl()));}

    /***
     * @param attacker the attacking character
     * This function models the standard interaction of a hammer attack on the enemy
     */
    protected void getStandardHammerAttacked(Players attacker) {minusHp(calculateDmg(1.5*seventyFivePercent(),attacker.getAtk(),def,attacker.getLvl()));}

}