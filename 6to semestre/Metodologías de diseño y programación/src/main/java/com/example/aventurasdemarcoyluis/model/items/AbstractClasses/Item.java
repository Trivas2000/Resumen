package com.example.aventurasdemarcoyluis.model.items.AbstractClasses;

import com.example.aventurasdemarcoyluis.model.items.interfaces.useItem;

import java.util.Objects;

/***
 * General abstract class for all items
 */
public abstract class Item implements useItem {


    private String name;

    private int amount;
    /***
     * Starts the amount at 0
     * @param itemName The name associated with the item
     */
    public Item(String itemName) {
        name = itemName;
        amount = 0;}


    /**
     * @return the item amount
     */
    public int getAmount() {return this.amount;}
    /**
     * @return the item name
     */
    public String getName() {return this.name;}

    /***
     * sets a new value for amount
     * @param newAmount new value for amount
     */
    public void setAmount(int newAmount) {this.amount=newAmount;}
    /***
     * Adds an amount to the current amount
     * @param addition the extra amount we are adding
     */
    public void add(int addition) {this.amount += addition;}

    /***
     * Override to the equals method, when to items have the same name and amount they are considered equals
     * @param o the item we are comparing to
     * @return True if they have the same values, false otherwise
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Item item = (Item) o;
        return amount == item.amount && Objects.equals(name, item.name);
    }
}
