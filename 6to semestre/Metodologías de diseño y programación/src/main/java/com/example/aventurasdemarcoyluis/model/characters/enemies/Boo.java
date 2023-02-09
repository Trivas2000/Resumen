package com.example.aventurasdemarcoyluis.model.characters.enemies;

import com.example.aventurasdemarcoyluis.model.characters.AbstractClasses.AbstractEnemies;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.AttackedByBoo;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.HammerAttackedByMarco;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;
import com.example.aventurasdemarcoyluis.model.game.patterns.visitors.CharacterVisitor;
import com.example.aventurasdemarcoyluis.model.game.patterns.visitors.EnemiesVisitor;

/**
 * Boo is a ghost like enemy that has specific restrictions with
 * the players who can attack him and whom he can attack
 */
public class Boo extends AbstractEnemies implements HammerAttackedByMarco {
    /***
     * @param ATK Amount of attack points
     * @param DEF Amount of defense points
     * @param maxHp amount of hit points
     * @param LVL Current character level
     * The enemy type is Boo by default
     */
    public Boo(int ATK, int DEF, int maxHp, int LVL) {
        super(ATK, DEF, maxHp, LVL, "Boo");
    }


    /***
     * The boo accepts a visitor
     * @param enemiesVisitor the visitor to accept
     */
    @Override
    public void accept(EnemiesVisitor enemiesVisitor) {enemiesVisitor.visitBoo(this);
    }


    /***
     * The boo accepts a visitor
     * @param visitor the visitor to accept
     */
    @Override
    public void acceptGeneral(CharacterVisitor visitor) {visitor.visitBoo(this);
    }

    /***
     * Simulates boo attacking a player
     * @param player the player getting attacked
     */

    public void attacks(AttackedByBoo player) {if (!isKod()){player.getsAttackedByBoo(this);}}

    /***
     * @param attacker the attacking character
     * This function models the interaction of Boo getting attacker by Marco
     */
    @Override
    public void getsJumpAttackedByMarco(Marco attacker) {minusHp(calculateDmg(1,attacker.getAtk(),def,attacker.getLvl()));}

    /***
     * Empty method because it dodges the attack
     * @param attacker Marco that attacks the boo
     */
    @Override
    public void getsHammerAttackedByMarco(Marco attacker) {

    }
    }

