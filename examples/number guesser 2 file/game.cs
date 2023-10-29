
using System;

namespace NumGuess2
{
    class Program
    {
        static void Main()
        {
            Console.WriteLine("Welcome to number guesser!");
            while (true)
            {
                sissyphusRollingBoulderUpHill();
            }
        }
        static void sissyphusRollingBoulderUpHill()
        {
            Console.WriteLine("I'm thinking of a number between 1 and 100...");
            Guess guesser = new Guess(new Random().Next(1, 101));
            while (!guesser.guessing())
            {
                Console.WriteLine("Try again...");
            }
            Console.WriteLine("Thanks for playing!\n"); //  2 line spacing before restart looks nice  //
        }
    }
}