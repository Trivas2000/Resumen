package com.example.aventurasdemarcoyluis.model.characters.enemies;

import com.example.aventurasdemarcoyluis.model.characters.AbstractClasses.AbstractEnemies;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.HammerAttackedByLuis;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.JumpedAttackedByLuis;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.HammerAttackedByMarco;
import com.example.aventurasdemarcoyluis.model.characters.interfaces.Players;
import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;
import com.example.aventurasdemarcoyluis.model.game.patterns.visitors.CharacterVisitor;
import com.example.aventurasdemarcoyluis.model.game.patterns.visitors.EnemiesVisitor;

/***
 * Spiny is a turtle like enemy that can only be hurt through hammer attacks. Jumping on it diminishes the players health
 */
public class Spiny extends AbstractEnemies  implements JumpedAttackedByLuis, HammerAttackedByMarco, HammerAttackedByLuis {
    /***
     * @param ATK Amount of attack points
     * @param DEF Amount of defense points
     * @param maxHp amount of hit points
     * @param LVL Current character level
     * The enemy type is Spiny by default
     */
    public Spiny(int ATK, int DEF, int maxHp, int LVL) {
        super(ATK, DEF, maxHp, LVL, "Spiny");
    }

    /***
     * Instead of Spiny receiving damage, the attacker gets damaged by 5% of its maxHp
     * Models Luis jump attacking Spiny
     * @param attacker the character attacking Spiny
     */
    @Override
    public void getsJumpAttackedByLuis(Luis attacker) {attacker.minusHp((int) (attacker.getMaxHp()*0.05));}

    /***
     * Instead of Spiny receiving damage, the attacker gets damaged by 5% of its maxHp
     * Models Marco jump attacking Spiny
     * @param attacker the character attacking Spiny
     */
    @Override
    public void getsJumpAttackedByMarco(Marco attacker) {attacker.minusHp((int) (attacker.getMaxHp()*0.05));}

    /***
     * This functions makes Spiny attack the player
     * @param player the player getting attacked
     */

    public void attacks(Players player) {if (!isKod()){player.getsAttackedBySpiny(this);}}

    /** Models Marco hammer attacking Spiny
     * @param attacker the character attacking Spiny
     */
    @Override
    public void getsHammerAttackedByMarco(Marco attacker) {getStandardHammerAttacked(attacker);}

    /** Models Luis hammer attacking Spiny
     * @param attacker the character attacking Spiny
     */
    @Override
    public void getsHammerAttackedByLuis(Luis attacker) {getStandardHammerAttacked(attacker);}

    /***
     * The spiny accepts a visitor
     * @param enemiesVisitor the visitor to accept
     */
    @Override
    public void accept(EnemiesVisitor enemiesVisitor) {enemiesVisitor.visitSpiny(this);

    }


    /***
     * The boo accepts a visitor
     * @param visitor the visitor to accept
     */
    @Override
    public void acceptGeneral(CharacterVisitor visitor) {visitor.visitSpiny(this);
    }
}
