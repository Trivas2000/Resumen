import com.example.aventurasdemarcoyluis.model.characters.players.Luis;
import com.example.aventurasdemarcoyluis.model.characters.players.Marco;
import com.example.aventurasdemarcoyluis.model.items.AbstractClasses.Item;
import com.example.aventurasdemarcoyluis.model.items.Arsenal;
import com.example.aventurasdemarcoyluis.model.items.RedMushroom;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestItems {

    private Item testItem;
    private Luis testLuis;
    private Marco testMarco;

    @BeforeEach
    public void setUp() {

        testLuis = new Luis(10, 20, 201, 120, 1);
        testMarco = new Marco(10, 20, 201, 120, 1);
        testItem = new RedMushroom();

    }

    @Test
    public void constructorTestArsenal() {
        assertTrue(testLuis.isInArsenal("Red Mushroom"));
        assertFalse(testLuis.isInArsenal("Pikachu"));
        assertEquals(0, testLuis.itemAmount("Red Mushroom"));
        assertFalse(testLuis.hasItem("Red Mushroom"));
        testLuis.addItem("Red Mushroom", 1);
        assertTrue(testLuis.hasItem("Red Mushroom"));
        assertTrue(testLuis.isInArsenal("Red Mushroom"));
        assertEquals(1, testLuis.itemAmount("Red Mushroom"));
        testLuis.addItem("Honey Syrup", 10);
        assertTrue(testLuis.isInArsenal("Honey Syrup"));
        assertTrue(testLuis.hasItem("Honey Syrup"));
        testLuis.addItem("Honey Syrup", -10);
        assertTrue(testLuis.isInArsenal("Honey Syrup"));
        assertFalse(testLuis.hasItem("Honey Syrup"));
        testLuis.addItem("Honey Syrup", 0);
        assertTrue(testLuis.isInArsenal("Honey Syrup"));
        testLuis.addItem("Honey Syrup", -1);
        assertTrue(testLuis.isInArsenal("Honey Syrup"));

    }

    @Test
    public void constructorTestItems() {
        assertEquals("Red Mushroom", testItem.getName());
        assertEquals(0, testItem.getAmount());
        testItem.add(10);
        assertEquals(10, testItem.getAmount());
        testItem.setAmount(0);
        assertEquals(0, testItem.getAmount());
    }

    @Test
    public void addExistingItemTest() {
    Arsenal testArsenal=new Arsenal();
    RedMushroom testRedMushroom = new RedMushroom();
    testRedMushroom.add(100);
    testLuis.setItems(testArsenal);
    assertEquals(0,testLuis.itemAmount("Red Mushroom"));
    testLuis.addItem("Red Mushroom",1);
    assertEquals(1,testLuis.itemAmount("Red Mushroom"));
    testArsenal.addItem(testRedMushroom);
    assertEquals(1,testLuis.itemAmount("Red Mushroom"));


    }
    @Test
    public void itemUseTestRM() {
        assertEquals(0, testLuis.itemAmount("Red Mushroom"));
        testLuis.setHp(0);
        testLuis.addItem("Red Mushroom", 2);
        assertEquals(2, testLuis.itemAmount("Red Mushroom"));
        testLuis.useItem("Red Mushroom");
        assertEquals(1, testLuis.itemAmount("Red Mushroom"));
        assertEquals(20, testLuis.getHp());
        assertEquals(201, testLuis.getMaxHp());
        testLuis.setHp(201);
        testLuis.useItem("Red Mushroom");
        assertEquals(0, testLuis.itemAmount("Red Mushroom"));
        assertEquals(201, testLuis.getHp());

    }

    @Test
    public void itemUseTestHS() {
        assertEquals(0, testLuis.itemAmount("Honey Syrup"));
        testLuis.setFp(0);
        testLuis.addItem("Honey Syrup", 2);
        assertEquals(2, testLuis.itemAmount("Honey Syrup"));
        testLuis.useItem("Honey Syrup");
        assertEquals(1, testLuis.itemAmount("Honey Syrup"));
        assertEquals(3, testLuis.getFp());
        assertEquals(120, testLuis.getMaxFp());
        testLuis.setFp(119);
        testLuis.useItem("Honey Syrup");
        assertEquals(0, testLuis.itemAmount("Honey Syrup"));
        assertEquals(120, testLuis.getFp());
    }

    @Test
    /**This test is specifically for testing a shared arsenal between 2 main characters
     */
    public void sharedArsenal() {
        Arsenal sharedArsenal = new Arsenal();
        testMarco.setItems(sharedArsenal);
        testLuis.setItems(sharedArsenal);

        assertEquals(0, testLuis.itemAmount("Honey Syrup"));
        assertEquals(0, testMarco.itemAmount("Honey Syrup"));
        testLuis.setFp(0);
        testLuis.addItem("Honey Syrup", 2);
        assertEquals(2, testMarco.itemAmount("Honey Syrup"));
        assertEquals(2, testLuis.itemAmount("Honey Syrup"));

        testLuis.useItem("Honey Syrup");
        assertEquals(1, testLuis.itemAmount("Honey Syrup"));
        assertEquals(1, testMarco.itemAmount("Honey Syrup"));
        assertEquals(3, testLuis.getFp());
        testMarco.setFp(119);

        testMarco.useItem("Honey Syrup");
        assertEquals(0, testLuis.itemAmount("Honey Syrup"));
        assertEquals(0, testMarco.itemAmount("Honey Syrup"));
        assertEquals(120, testMarco.getFp());
        }

}
