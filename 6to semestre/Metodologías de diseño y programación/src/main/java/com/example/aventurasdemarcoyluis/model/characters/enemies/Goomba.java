package com.example.aventurasdemarcoyluis.model.characters.enemies;

import com.example.aventurasdemarcoyluis.model.characters.AbstractClasses.AbstractEnemies;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.Character;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.HammerAttackedByMarco;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.HammerAttackedByLuis;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.JumpedAttackedByLuis;
import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.Players;
import com.example.aventurasdemarcoyluis.model.game.patterns.visitors.CharacterVisitor;
import com.example.aventurasdemarcoyluis.model.game.patterns.visitors.EnemiesVisitor;

/**
 * Goomba is a brown and small enemy. It is the most basic enemy in the game and is meant to be targeted by all attacks from all the players
 */
public class Goomba extends AbstractEnemies implements JumpedAttackedByLuis, HammerAttackedByMarco, HammerAttackedByLuis, Character {
    /***
     * @param ATK Amount of attack points
     * @param DEF Amount of defense points
     * @param maxHp amount of hit points
     * @param LVL Current character level
     * The enemy type is Goomba by default
     */
    public Goomba(int ATK, int DEF, int maxHp, int LVL) {
        super(ATK, DEF, maxHp, LVL, "Goomba");
    }

    /***
     * @param attacker the attacking character
     * This function models the interaction of Goomba getting attacker by Marco
     */
    @Override
    public void getsJumpAttackedByMarco(Marco attacker) {getStandardJumpedAttacked(attacker);}

    /***
     * The goomba accepts a visitor
     * @param enemiesVisitor the visitor to accept
     */
    @Override
    public void accept(EnemiesVisitor enemiesVisitor) {enemiesVisitor.visitGoomba(this);

    }


    /***
     * The goomba accepts a visitor
     * @param visitor the visitor to accept
     */
    @Override
    public void acceptGeneral(CharacterVisitor visitor) {visitor.visitGoomba(this);
    }

    /***
     * @param attacker the attacking character
     * This function models the interaction of Goomba getting attacker by Luis
     */
    @Override
    public void getsJumpAttackedByLuis(Luis attacker) {getStandardJumpedAttacked(attacker);}

    /***
     * This functions makes Goomba attack the player
     * @param player the player getting attacked
     */
    public void attacks(Players player){if (!isKod()){player.getsAttackedByGoomba(this);}}

    /** Models Marco attacking Goomba
     * @param attacker the character attacking Goomba
     */
    @Override
    public void getsHammerAttackedByMarco(Marco attacker) {getStandardHammerAttacked(attacker);}

    /** Models Luis hammer attacking Goomba
     * @param attacker the character attacking Goomba
     */
    @Override
    public void getsHammerAttackedByLuis(Luis attacker) {getStandardHammerAttacked(attacker);}

}

