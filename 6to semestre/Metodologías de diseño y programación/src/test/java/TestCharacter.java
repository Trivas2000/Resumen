
import com.example.aventurasdemarcoyluis.model.characters.enemies.Boo;
import com.example.aventurasdemarcoyluis.model.characters.enemies.Goomba;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestCharacter {

    private Goomba testGoomba;
    private Boo testBoo;
    private Marco testMarco;

    @BeforeEach
    public void setUp() {
        testGoomba = new Goomba(2, 10, 15, 8);
        testBoo = new Boo(5, 9, 150, 8);
        testMarco = new Marco(10, 20, 200, 12, 1);
    }

    @Test
    public void constructorTestEnemies() {
        assertEquals("Boo", testBoo.getType());
        assertEquals("Goomba", testGoomba.getType());
        assertEquals(2, testGoomba.getAtk());
        assertEquals(15, testGoomba.getMaxHp());
        assertEquals(15, testGoomba.getHp());
        testGoomba.setDef(89);
        assertEquals(89, testGoomba.getDef());

    }

    @Test
    public void gettersAndSetterTest() {
        testGoomba.setAtk(8);
        assertEquals(8, testGoomba.getAtk());
        testBoo.setHp(100);
        assertEquals(100, testBoo.getHp());
        assertEquals(150, testBoo.getMaxHp());
        testMarco.setHp(-100);
        assertEquals(0, testMarco.getHp());
        testGoomba.setHp(400);
        assertEquals(15, testGoomba.getHp());
        assertEquals(15, testGoomba.getMaxHp());
    }
    @Test

    public void constructorTestPlayers() {
        assertEquals(20, testMarco.getDef());
        assertEquals(2, testGoomba.getAtk());
        assertEquals(15, testGoomba.getMaxHp());
        assertEquals(15, testGoomba.getHp());
    }

    @Test

    public void isKodTest(){
        testMarco.setHp(10);
        testGoomba.setHp(25);
        assertFalse(testMarco.isKod());
        assertFalse(testGoomba.isKod());
        testMarco.setHp(-500);
        testGoomba.setHp(-1);
        assertTrue(testMarco.isKod());
        assertTrue(testGoomba.isKod());
        testMarco.setHp(0);
        testGoomba.setHp(0);
        assertTrue(testMarco.isKod());
        assertTrue(testGoomba.isKod());
    }

    @Test

    public void lvlUpTest(){
        testMarco.setAtk(100);
        assertEquals(100,testMarco.getAtk());
        assertEquals(200,testMarco.getMaxHp());
        assertEquals(12,testMarco.getFp());
        assertEquals(200,testMarco.getMaxHp());
        assertEquals(200,testMarco.getHp());
        assertEquals(20,testMarco.getDef());
        assertEquals(1,testMarco.getLvl());

        testMarco.lvlUp();
        assertEquals(115,testMarco.getAtk());
        assertEquals(230,testMarco.getMaxHp());
        assertEquals(14,testMarco.getFp());
        assertEquals(230,testMarco.getMaxHp());
        assertEquals(24,testMarco.getDef());
        assertEquals(2,testMarco.getLvl());

    }
}
