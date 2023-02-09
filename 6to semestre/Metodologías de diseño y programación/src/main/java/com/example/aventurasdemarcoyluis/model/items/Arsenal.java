
package com.example.aventurasdemarcoyluis.model.items;


import com.example.aventurasdemarcoyluis.model.characters.interfaces.Players;
import com.example.aventurasdemarcoyluis.model.items.interfaces.useItem;

import java.util.*;

/***
 * This class simulates an arsenal for the players, where they have various items with their respective amounts.
 */

public class Arsenal {
    /***
     * itemList the array list of all the items currently in possession.
     */
    private ArrayList<useItem> itemList;

    /**
     * By default, we add 2 items,RedMushroom and Honey Syrup; but it is open for expansions and more items.
     */

    public Arsenal() {

        itemList = new ArrayList<>();
        itemList.add(new RedMushroom());
        itemList.add(new HoneySyrup());
    }

    /***
     * Checks if an item is in the current arsenal
     * @param item the item we are looking for
     * @return true if the item is in it, false if not
     */
    public boolean isInList(String item) {
        int counter = 0;
        while (itemList.size() > counter) {
            if (itemList.get(counter).getName() == item) {
                return true;
            }
            counter += 1;
        }
        return false;
    }

    /***
     * @param item the item we want the index for
     * @return the index of the item, if it is not in the list returns -1
     */
    private int getIndex(String item) {
        int counter = 0;
        while (itemList.size() > counter) {
            if (itemList.get(counter).getName() == item) {
                return counter;
            }
            counter += 1;
        }
        return -1;
    }

    /***
     * @param item the item we want the amount of
     * @return item amount
     */
    public int getAmount(String item) {
        return itemList.get(getIndex(item)).getAmount();
    }

    /**
     * Adds amount to  a certain item in the arsenal
     *
     * @param item   the item we want to add amount to
     * @param amount the amount we want to add
     */
    public void addAmount(String item, int amount) {
        itemList.get(getIndex(item)).add(amount);
    }

    /***
     * Uses the item on the player
     * @param item the item the player is using
     * @param player the player that is using the item
     */
    public void use(String item, Players player) {
        addAmount(item,-1);
        itemList.get(getIndex(item)).useItem(player);
    }

    /***
     * If the item is not in the arsenal it adds it.
     * @param item the item we want to add
     */
    public void addItem(useItem item) {
        if (!isInList(item.getName())) {
            itemList.add(item);}}

    /***
     * Returns the complete array with all the items
     * @return the item array
     */
    public ArrayList<useItem> getItemList() {
        return itemList;
    }



}


