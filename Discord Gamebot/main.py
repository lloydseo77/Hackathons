#Add the bot to a server using this link: https://discord.com/api/oauth2/authorize?client_id=965124636004200488&permissions=8&scope=bot
#Run the code to get the bot online
#Have fun!
#Our submission is a discord bot with 6 unique commands that use the prefix '$'
#The commands are as follows:
# help: displays the command directory
# greet: allows the user to exchange greetings with the bot
# blackjack: plays a round of blackjack with the user
# guessNum: starts a game of guessing a number between 0 and 100
# wordle: inspired by the recent hit game, Wordle!
# rps: plays a quick game of 'rock, paper, scissors!' with the user

import discord
from wonderwords import RandomWord
import os
from dotenv import load_dotenv
from discord.ext import commands
import random
r = RandomWord()

load_dotenv()
secret = os.getenv('token')

bot = commands.Bot(command_prefix="$")
bot.remove_command('help')


#***************************************************
#HELP COMMAND
#creates an embed that describes each command
@bot.command(pass_context = True)
async def help(message):
  eHelp = discord.Embed(colour=discord.Colour.blue())
  eHelp.set_author(name = 'Command Directory')
  eHelp.add_field(name = '$help', value = 'Shows this message',inline = False)
  eHelp.add_field(name = '$greet', value = 'Gives a greeting',inline = False)
  eHelp.add_field(name = '$rps',value = 'Play a game of Rock Paper Scissors with the computer.',inline = False)
  eHelp.add_field(name = '$guessNum',value = 'Guess a number between 0-100 in the least amount of tries.',inline = False)
  eHelp.add_field(name = '$wordle', value = 'Play Wordle',inline = False)
  eHelp.add_field(name = '$blackjack', value = "Play a round of Blackjack against the dealer/computer",inline = False)
  await message.channel.send(embed=eHelp)
  
#***************************************************
#GREET COMMAND
@bot.command()
async def greet(message):
    await message.send("Say hello!")

    def check(m):
        return m.author == message.author and m.channel == message.channel 

    msg = await bot.wait_for("message", check=check)
    await message.send(f"Hello {msg.author}!")


#***************************************************
#BLACKJACK COMMAND
@bot.command()
async def blackjack(message):
  eBlack = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))
  eBlack.add_field(name = "Blackjack", value = "Get as close to 21 without going over to win!", inline = True)

  await message.channel.send(embed=eBlack)
  def check(m):
    return m.author == message.author and m.channel == message.channel

  def checkRoyal(cardArg):
      if card == 1:
        return "Ace"
      elif card == 11:
        return "Jack"
      elif card == 12:
        return "Queen"
      elif card == 13:
        return "King"
      else:
        return cardArg

  def getSuit():
    r = random.randint(1,4)
    if r == 1:
      return "❤"
    elif r == 2:
      return "♦️"
    elif r == 3:
      return "♠️ "
    elif r == 4:
      return "♣️"
      
  playerHand = []
  compHand = []

  card = random.randint(1, 13) #randomize
  turn = 0
  
  eBlack1 = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))
  
  compHand.append(card) #cpu draw
  eBlack1.set_author(name = "Blackjack")
  eBlack1.add_field(name = "CPU Card " + str(turn + 1), value = str(checkRoyal(compHand[turn])) + getSuit(), inline = True)
  card = random.randint(1, 13)
  
  compHand.append(card)
  eBlack1.add_field(name = "CPU Card " + str(turn + 2), value = "???", inline = True)
  card = random.randint(1, 13)
  
  playerHand.append(card)
  eBlack1.add_field(name = "Player Card " + str(turn + 1), value = str(checkRoyal(playerHand[turn])) + getSuit(), inline = False)

  turn += 1
  card = random.randint(1, 13)
  
  playerHand.append(card) #player draw
  eBlack1.add_field(name = "Player Card " + str(turn + 1), value = str(checkRoyal(playerHand[turn])) + getSuit(), inline = True)
  
  eBlack1.set_footer(text = "Hit or Stand? (H/S)")
  
  await message.channel.send(embed=eBlack1) #print current card holdings
  turn += 1
  
  again = True

  def hasAce(hand):
    for i in hand: #search for ace in player hand
      ace = False
      if i == 1:
        ace = True
      return ace

  compScore = sum(compHand)
  if hasAce(compHand) and compScore + 10 <= 21: #change ace from 1 to 11
    compScore += 10

  playerLoss = False
  
  compLoss = False
  if compScore > 21: #determines if cpu loses
    compLoss = True

  while again:
    
    playerScore = sum(playerHand)
    if hasAce(playerHand) and playerScore <= 21: #change ace from 1 to 11
      playerScore += 10

    eBlackPlayerScore = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))
    eBlackPlayerScore.add_field(name = "Player Score", value = str(playerScore), inline = True)
    await message.channel.send(embed=eBlackPlayerScore)
    
    choice = await bot.wait_for("message", check=check) #get user-input
    if choice.content == "h" or choice.content == "H": #hit
      playerHand.append(random.randint(1, 13)) #draw
      eBlack1.add_field(name = "Player Card " + str(turn + 1), value = str(checkRoyal(playerHand[turn])) + getSuit(), inline = True) #change card holdings embed
      playerScore += playerHand[turn]
      turn += 1
      await message.channel.send(embed=eBlack1) #print card holdings embed
    elif choice.content == "s" or choice.content == "S": #stand
      again = False
    else:
      eBlackError = discord.Embed(colour=discord.Colour.from_rgb(143, 3, 3))
      eBlackError.add_field(name = "Blackjack", value = "Please enter H or S.")
      await message.channel.send(embed=eBlackError)

    if playerScore > 21:
      if hasAce(playerHand): #if player went over 21 and has an ace, treat it as 1 instead of 11
        playerScore -= 10
      else:
        again = False
        playerLoss = True

  eBlackPlayerScore = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))
  eBlackPlayerScore.add_field(name = "Player Score", value = str(playerScore), inline = True)
  await message.channel.send(embed=eBlackPlayerScore)

  eBlackCompScore = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))
  eBlackCompScore.add_field(name = "CPU Score", value = str(compScore), inline = True)
  await message.channel.send(embed=eBlackCompScore)
  
  eBlackReveal = discord.Embed(colour=discord.Colour.from_rgb(226, 237, 241))
  eBlackReveal.add_field(name = "Blackjack", value = "CPU Card 2 was " + str(checkRoyal(compHand[1])))
  await message.channel.send(embed=eBlackReveal)
  
  eBlackWin = discord.Embed(colour=discord.Colour.from_rgb(226, 237, 241))
  if playerScore > compScore and playerScore <= 21 or compLoss: #player wins
    eBlackWin.add_field(name = "Blackjack", value = "You won!")
  elif playerScore < compScore and compScore <= 21 or playerLoss: #cpu wins
    eBlackWin.add_field(name = "Blackjack", value = "You lost...")
  elif playerScore == compScore or playerLoss and compLoss: #tie
    eBlackWin.add_field(name = "Blackjack", value = "You tied.")
  await message.channel.send(embed=eBlackWin) #print win embed

#***************************************************
#GUESS THE NUMBER (GUESSNUM) COMMAND
@bot.command()
async def guessNum(message):
  number = random.randint(0, 100)
  eNum1 = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))
  eNum1.add_field(name = "Number Guessing Game", value = "Enter a number between 0 and 100", inline = True)

  await message.channel.send(embed=eNum1)
  def check(m):
        return m.author == message.author and m.channel == message.channel
    
  win = False
  turncount = 1

  while win == False:
    eNum2 = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))
    guess = await bot.wait_for("message", check=check)
    if (int(guess.content) >= 0 and int(guess.content) <= 100): #validate input range
      if (int(guess.content) > number): #guess is greater
        eNum2.add_field(name = "Number Guessing Game", value = "Go Lower!", inline = True)
        turncount += 1
      elif (int(guess.content) < number): #guess is lower
        eNum2.add_field(name = "Number Guessing Game", value = "Go Higher!", inline = True)
        turncount += 1
      else: #guess is correct
        eNum2.add_field(name = "Number Guessing Game", value = "You got it right in " + str(turncount) + " tries!", inline = True)
        win = True
        turncount += 1
      await message.channel.send(embed=eNum2)


#***************************************************
#Error handling messages for the $wordle command
eWordleInvalid = discord.Embed(colour=discord.Colour.from_rgb(143, 3, 3))
eWordleInvalid.add_field(name = "Wordle", value = "Not a valid word. You can end the game by typing .end")

eWordleNumCorrection = discord.Embed(colour=discord.Colour.from_rgb(143, 3, 3))
eWordleNumCorrection.add_field(name = "Wordle", value = "Enter a 5-letter word")

eWordleEnd = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))
eWordleEnd.add_field(name = "Wordle", value = "Game ended")

eWordleWin = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))

#WORDLE COMMAND
@bot.command()
async def wordle(message):
  r = RandomWord() #generates random word
  poss = ["⬜","⬜","⬜","⬜","⬜"] #declares array that begins with blank spaces that will be filled from user inputs
  letterBank = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"] #declares a letter bank for the user to see what letters they have not yet used
  mismatched = [] #declares a letter bank for letters that have been correctly guessed, but in the wrong place
  word = r.word(word_min_length=5,word_max_length=5)
  #embeds the prompt
  eWordleWin.set_author(name = "The word was " + word)
  eWordle = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))
  eWordle.set_author(name = "Wordle")
  eWordle.add_field(name = (' '.join([str(elem) for elem in poss])), value = "Enter a guess! Each guess must be a valid 5-letter word. You can end the game by typing .end", inline = True)
  await message.channel.send(embed=eWordle)
  def check(m):
    return m.author == message.author and m.channel == message.channel

  
  while "⬜" in poss: #loops until all letters have been guessed correctly
    verify = 0
    attempt = await bot.wait_for("message", check=check) #waits for guess
    
    if attempt.content.startswith(".end"):
      await message.channel.send(embed=eWordleEnd)
      break
    else:
      response = (str(attempt.content)).lower()
      file = open("Wordle.txt","r")
      for line in file: #verifies if input is a valid word
        if response in line:
          verify = 1

      #checks if letters in input matches the randomly generated word; updates mismatched and letterBank
      if len(response) == 5 and verify == 1:
        for i in range(0,5):
          if word[i:i+1] == response[i:i+1]:
            poss[i] = word[i:i+1]
            if word[i:i+1] in mismatched:
              mismatched.remove(word[i:i+1])
          if response[i:i+1] in word and response[i:i+1] not in mismatched and word[i:i+1] != response[i:i+1] and response[i:i+1] not in poss: 
            mismatched.append(response[i:i+1])
          if response[i:i+1] in letterBank:
            letterBank.remove(response[i:i+1])

        #sends embed with updated prompt
      eWordle1 = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))
      eWordle1.add_field(name = "Wordle", value = ' '.join([str(elem) for elem in poss]), inline = False)
      eWordle1.add_field(name = "Letters in wrong space:", value = "-" + ' '.join([str(elem) for elem in mismatched]), inline = False)
      eWordle1.add_field(name = "Letter Bank: ", value = ' '.join([str(elem) for elem in letterBank]), inline = False)
      await message.channel.send(embed=eWordle1)
      
      #sends embedded error messages
      if verify == 0:
        await message.channel.send(embed=eWordleInvalid)
      elif len(response) != 5:
        await message.channel.send(embed=eWordleNumCorrection)
        
    if "⬜" not in poss:
      break
    file.close()
  await message.channel.send(embed=eWordleWin)
  
  

#***************************************************
#ROCK PAPER SCISSORS (RPS) COMMAND
@bot.command()
async def rps(message):
  

  eRps1 = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))
  eRps1.add_field(name = "Rock Paper Scissors", value = "Input rock, paper, or scissor.", inline = True)
  
  await message.channel.send(embed=eRps1)
  def check(m):
        return m.author == message.author and m.channel == message.channel
  
  file1 = open("rspStats.txt", "r+")
  msg = await bot.wait_for("message", check=check)
  if (str(msg.content) == "rock"):
    player = 3
    file1.write(msg.content + "\n")
  elif (str(msg.content) == "scissor"):
    player = 2
    file1.write(msg.content + "\n")
  elif (str(msg.content) == "paper"):
    player = 1
    file1.write(msg.content + "\n")
  
  rock = paper = scissor = 0
  for line in file1:
    if "paper" in line:
      paper += 1
    elif "scissor" in line:
      scissor += 1
    else:
      rock += 1
  file1.close()

  if rock > scissor and rock > paper:
    num = 1
  elif scissor > rock and scissor > paper:
    num = 3
  elif paper > rock and paper > scissor:
    num = 2
  elif rock == paper:
    num = random.randint(1, 2)
  elif rock == scissor:
    num = random.randint(1, 2)
    if num == 2:
      num = 3
  elif scissor == paper:
    num = random.randint(2, 3)
  else: 
    num = random.randint(1, 3) #paper = 1, scissors = 2, rock = 3
  

    
  eRps2 = discord.Embed(colour=discord.Colour.from_rgb(107, 212, 205))
  
  if player == num:
    eRps2.add_field(name = "Rock Paper Scissors", value = "Tie!", inline = True)
  elif (num == player + 1) or (num == 1 and player == 3):
    if num == 1:
      eRps2.add_field(name = "Rock Paper Scissors", value = "Bot Wins by using paper!", inline = True)
    elif num == 2:
      eRps2.add_field(name = "Rock Paper Scissors", value = "Bot Wins by using scissor!", inline = True)
    else:
      eRps2.add_field(name = "Rock Paper Scissors", value = "Bot Wins by using rock!", inline = True)
  else:
    eRps2.add_field(name = "Rock Paper Scissors", value = f" {msg.author}!" + " wins!", inline = True)
  await message.channel.send(embed=eRps2)

#***************************************************
#Runs the bot using the secret token (system environmental variable)
bot.run(secret)