import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Spiny;
import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;
import com.example.aventurasdemarcoyluis.model.game.BattleSimulator;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidActionException;
import com.example.aventurasdemarcoyluis.model.game.exceptions.InvalidPhaseTransitionException;
import com.example.aventurasdemarcoyluis.model.game.patterns.phases.EndTurnPhase;
import com.example.aventurasdemarcoyluis.model.items.Arsenal;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class PhasesTest {
    private BattleSimulator testBattleSimulator;
    private Marco testMarco;
    private Luis testLuis;
    private Spiny testSpiny;
    private Boo testBoo;
    private Goomba testGoomba;

    @BeforeEach
    public void setUp() {

        testSpiny = new Spiny(5, 15, 10, 1);
        testBoo = new Boo(5, 5, 10, 1);
        testGoomba = new Goomba(10, 10, 10, 1);
        testMarco=new Marco(20,10,20,20,1);
        testLuis=new Luis(10,20,20,20,1);

        ArrayList<Integer> enemiesIndex;
        enemiesIndex = new ArrayList();
        enemiesIndex.add(1);
        enemiesIndex.add(2);
        enemiesIndex.add(3);
        testBattleSimulator = new BattleSimulator(1,enemiesIndex);
    }

    /***
     *
     * Goomba attack marco seed 12210
     * Spiny attack luis seed 120
     */
    @RepeatedTest(100)
    public void passPhaseTest() throws InvalidPhaseTransitionException {
        testBattleSimulator.startGame();
        assertEquals("Start of player turn Phase",testBattleSimulator.getPhase().toString());
        assertEquals(testBattleSimulator.currentTurnCharacter(),testMarco);
        testBattleSimulator.passTurn();
        assertEquals(testBattleSimulator.currentTurnCharacter(),testLuis);
        assertEquals("Start of player turn Phase",testBattleSimulator.getPhase().toString());
        assertEquals(20,testBattleSimulator.playersGetter(0).getHp());
        assertEquals(20,testBattleSimulator.playersGetter(1).getHp());
        testBattleSimulator.enemiesGetter(0).setSeed(12210);
        testBattleSimulator.enemiesGetter(1).setSeed(120);
        testBattleSimulator.passTurn();
        assertEquals("Start of player turn Phase",testBattleSimulator.getPhase().toString());
        assertEquals(17,testBattleSimulator.playersGetter(0).getHp());
        assertEquals(18,testBattleSimulator.playersGetter(1).getHp());

    }

    @Test
    public void attackPhaseTest() throws InvalidPhaseTransitionException {
        testBattleSimulator.startGame();
        assertEquals("Start of player turn Phase",testBattleSimulator.getPhase().toString());
        assertEquals(testBattleSimulator.currentTurnCharacter(),testMarco);
        testBattleSimulator.chooseToAttack();
        assertEquals("Choosing attack type Phase",testBattleSimulator.getPhase().toString());
        testBattleSimulator.chooseJumpAttack();
        assertEquals("Player chooses enemy to attack Phase",testBattleSimulator.getPhase().toString());
        assertEquals(10,testBattleSimulator.enemiesGetter(0).getHp());
        testBattleSimulator.attackEnemy(0);
        assertEquals("Start of player turn Phase",testBattleSimulator.getPhase().toString());
        assertEquals(8,testBattleSimulator.enemiesGetter(0).getHp());

        assertEquals(testBattleSimulator.currentTurnCharacter(),testLuis);
        testBattleSimulator.chooseToAttack();
        assertEquals("Choosing attack type Phase",testBattleSimulator.getPhase().toString());
        testBattleSimulator.chooseHammerAttack();
        assertEquals("Player chooses enemy to attack Phase",testBattleSimulator.getPhase().toString());
        assertEquals(8,testBattleSimulator.enemiesGetter(0).getHp());
        testBattleSimulator.enemiesGetter(0).setSeed(7);
        testBattleSimulator.attackEnemy(0);
        assertEquals(7,testBattleSimulator.enemiesGetter(0).getHp());



    }

    @Test
    public void itemPhasesTest() throws InvalidPhaseTransitionException, InvalidActionException {
        testBattleSimulator.startGame();
        assertEquals(20,testBattleSimulator.playersGetter(0).getHp());
        assertEquals(20,testBattleSimulator.playersGetter(1).getHp());

        testBattleSimulator.addAmount("Red Mushroom",3);
        testBattleSimulator.addAmount("Honey Syrup",3);
        testBattleSimulator.damageCharacter(1,3);
        testBattleSimulator.damageCharacter(0,6);
        assertEquals(14,testBattleSimulator.playersGetter(0).getHp());

        assertEquals("Start of player turn Phase",testBattleSimulator.getPhase().toString());
        testBattleSimulator.chooseToUseItem();
        assertEquals("Player choose item Phase",testBattleSimulator.getPhase().toString());
        testBattleSimulator.chooseRedMushroom();
        assertEquals("Player choose who uses item Phase",testBattleSimulator.getPhase().toString());
        testBattleSimulator.chooseUseItemOnMarco();
        assertEquals("Start of player turn Phase",testBattleSimulator.getPhase().toString());

        assertEquals(16,testBattleSimulator.playersGetter(0).getHp());
        assertEquals(17,testBattleSimulator.playersGetter(1).getHp());

        testBattleSimulator.enemiesGetter(0).setSeed(1);
        testBattleSimulator.enemiesGetter(1).setSeed(1);
        testBattleSimulator.enemiesGetter(2).setSeed(1);

        assertEquals("Start of player turn Phase",testBattleSimulator.getPhase().toString());
        testBattleSimulator.chooseToUseItem();
        assertEquals("Player choose item Phase",testBattleSimulator.getPhase().toString());
        testBattleSimulator.chooseRedMushroom();
        assertEquals("Player choose who uses item Phase",testBattleSimulator.getPhase().toString());
        testBattleSimulator.chooseUseItemOnLuis();
        assertEquals("Start of player turn Phase",testBattleSimulator.getPhase().toString());

        /*** The enemies attack in between*/

        assertEquals(16,testBattleSimulator.playersGetter(1).getHp());
        assertEquals(20,testBattleSimulator.playersGetter(0).getFp());

        testBattleSimulator.chooseToAttack();
        testBattleSimulator.chooseJumpAttack();
        testBattleSimulator.attackEnemy(0);
        assertEquals(19,testBattleSimulator.playersGetter(0).getFp());
        testBattleSimulator.chooseToUseItem();
        testBattleSimulator.chooseHoneySyrup();
        testBattleSimulator.chooseUseItemOnMarco();
        assertEquals(20,testBattleSimulator.playersGetter(0).getFp());

    }

    @Test
    public void exceptionsTest() throws InvalidPhaseTransitionException {
        testBattleSimulator.startGame();
        assertThrows(InvalidPhaseTransitionException.class,()->testBattleSimulator.getPhase().transitionToEndTurnPhase());
        assertThrows(InvalidPhaseTransitionException.class,()->testBattleSimulator.getPhase().transitionToChoosingEnemyToAttackPhase());
        assertThrows(InvalidPhaseTransitionException.class,()->testBattleSimulator.getPhase().transitionToPlayerStartOfTurnPhase());
        assertThrows(InvalidPhaseTransitionException.class,()->testBattleSimulator.getPhase().transitionToNewTurnPhase());
        assertThrows(InvalidPhaseTransitionException.class,()->testBattleSimulator.getPhase().transitionToChoosingPLayerWhoUsesItemPhase());
        assertThrows(InvalidPhaseTransitionException.class,()->testBattleSimulator.getPhase().transitionToUsingItemPhase());
        assertThrows(InvalidPhaseTransitionException.class,()->testBattleSimulator.getPhase().transitionToEnemyAttackPhase());
        assertThrows(InvalidPhaseTransitionException.class,()->testBattleSimulator.getPhase().transitionEnemyToChooseTargetPhase());






        assertThrows(InvalidActionException.class,()->testBattleSimulator.getPhase().useItem());
        assertThrows(InvalidActionException.class,()->testBattleSimulator.getPhase().choosePlayer(12));
        assertThrows(InvalidActionException.class,()->testBattleSimulator.getPhase().chooseItem(1));
        assertThrows(InvalidActionException.class,()->testBattleSimulator.getPhase().playerPassTurn());
        assertThrows(InvalidActionException.class,()->testBattleSimulator.getPhase().phaseAttack(1));
        assertThrows(InvalidActionException.class,()->testBattleSimulator.getPhase().chooseAttackType(1));
        assertThrows(InvalidActionException.class,()->testBattleSimulator.getPhase().enemyPhaseAttack());
        assertThrows(InvalidActionException.class,()->testBattleSimulator.getPhase().chooseEnemyTarget());







    }


}
