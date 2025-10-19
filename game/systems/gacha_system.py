"""Gacha system for hero summoning"""
import random
from typing import List
from game.data.hero_data import Hero, get_heroes_by_rarity
from config import RARITY_RATES


class GachaSystem:
    """Handles hero summoning with rarity-based probability"""
    
    def __init__(self):
        """Initialize the gacha system with hero pools"""
        # Build hero pools by rarity
        self.hero_pool = {
            'rare': get_heroes_by_rarity('rare'),
            'legendary': get_heroes_by_rarity('legendary'),
            'extreme': get_heroes_by_rarity('extreme')
        }
        
        # Rarity rates from config
        self.rarity_rates = RARITY_RATES
        
        # Validate that we have heroes in each pool
        for rarity, heroes in self.hero_pool.items():
            if not heroes:
                raise ValueError(f"No heroes found for rarity: {rarity}")
    
    def calculate_rarity(self) -> str:
        """
        Calculate which rarity tier to summon from based on probability
        
        Returns:
            str: The rarity tier ('rare', 'legendary', or 'extreme')
        """
        # Generate random number between 0 and 1
        roll = random.random()
        
        # Check against cumulative probabilities
        cumulative = 0.0
        for rarity in ['extreme', 'legendary', 'rare']:
            cumulative += self.rarity_rates[rarity]
            if roll <= cumulative:
                return rarity
        
        # Fallback to rare (should never reach here if rates sum to 1.0)
        return 'rare'
    
    def get_random_hero(self, rarity: str = None) -> Hero:
        """
        Get a random hero from the specified rarity pool
        
        Args:
            rarity: Optional rarity tier. If None, calculates rarity randomly
            
        Returns:
            Hero: A randomly selected hero
        """
        # If no rarity specified, calculate it
        if rarity is None:
            rarity = self.calculate_rarity()
        
        # Get the hero pool for this rarity
        pool = self.hero_pool.get(rarity, self.hero_pool['rare'])
        
        # Return a random hero from the pool
        return random.choice(pool)
    
    def summon(self, count: int = 1) -> List[Hero]:
        """
        Perform a summon operation
        
        Args:
            count: Number of heroes to summon (1 for x1, 10 for x10)
            
        Returns:
            List[Hero]: List of summoned heroes
        """
        if count < 1:
            raise ValueError("Summon count must be at least 1")
        
        summoned_heroes = []
        for _ in range(count):
            hero = self.get_random_hero()
            summoned_heroes.append(hero)
        
        return summoned_heroes