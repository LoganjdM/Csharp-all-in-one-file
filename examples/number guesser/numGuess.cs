using System;

namespace NumberGuessGame
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Welcome to the Number Guessing Game!");
            Console.WriteLine("I'm thinking of a number between 1 and 100.");

            Random random = new Random();
            int secretNumber = random.Next(1, 101);
            int attempts = 0;

            bool hasGuessedCorrectly = false;

            while (!hasGuessedCorrectly)
            {
                Console.Write("Enter your guess: ");
                if (int.TryParse(Console.ReadLine(), out int guess))
                {
                    attempts++;
                    if (guess == secretNumber)
                    {
                        Console.WriteLine($"Congratulations! You guessed the number {secretNumber} in {attempts} attempts.");
                        hasGuessedCorrectly = true;
                    }
                    else if (guess < secretNumber)
                    {
                        Console.WriteLine("Try a higher number.");
                    }
                    else
                    {
                        Console.WriteLine("Try a lower number.");
                    }
                }
                else
                {
                    Console.WriteLine("Invalid input. Please enter a valid number.");
                }
            }

            Console.WriteLine("Thanks for playing!");
        }
    }
}