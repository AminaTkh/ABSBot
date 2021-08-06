
import random


class Bot(object):


	def __init__(self):
		self.name = "..."  # Put your id number her. String or integer will both work
		# Add your own variables here, if you want to.

	
	def get_bid_game_type_collection(self, current_round, bots, game_type, winner_pays, artists_and_values, round_limit,
		starting_budget, painting_order, target_collection, my_bot_details, current_painting, winner_ids, amounts_paid):
		"""Strategy for collection type games.

		Parameters:
		current_round(int): 			The current round of the auction game
		bots(dict): 					A dictionary holding the details of all of the bots in the auction
										For each bot, you are given these details:
										bot_name(str):		The bot's name
										bot_unique_id(str):	A unique id for this bot
										paintings(dict):	A dict of the paintings won so far by this bot
										budget(int):		How much budget this bot has left
										score(int):			Current value of paintings (for value game)
		game_type(str): 				Will be "collection" for collection type games
		winner_pays(int):				Rank of bid that winner plays. 1 is 1st price auction. 2 is 2nd price auction.
		artists_and_values(dict):		A dictionary of the artist names and the painting value to the score (for value games)
		round_limit(int):				Total number of rounds in the game - will always be 200
		starting_budget(int):			How much budget each bot started with - will always be 1001
		painting_order(list str):		A list of the full painting order
		target_collection(list int):	A list of the type of collection required to win, for collection games - will always be [3,2,1]
										[5] means that you need 5 of any one type of painting
										[4,2] means you need 4 of one type of painting and 2 of another
										[3,2,1] means you need 3 of one type of painting, 2 of another, and 1 of another
		my_bot_details(dict):			Your bot details. Same as in the bots dict, but just your bot.
										Includes your current paintings, current score and current budget
		current_painting(str):			The artist of the current painting that is being bid on
		winner_ids(list str):			A list of the ids of the winners of each round so far
		amounts_paid(list int):			List of amounts paid for paintings in the rounds played so far

		Returns:
		int:Your bid. Return your bid for this round.
		"""

		# WRITE YOUR STRATEGY HERE FOR COLLECTION TYPE GAMES - FIRST TO COMPLETE A FULL COLLECTION

		my_collection = my_bot_details["paintings"]
		my_budget = my_bot_details["budget"]
		kol3 = 0
		kol2 = 0
		kol1 = 0
		kol0 = 0
		
		for painting in my_collection:
			if my_collection[painting] >= 3:
				kol3 += 1
			if my_collection[painting] == 2:
				kol2 += 1
			if my_collection[painting] == 1:
				kol1 += 1
			if my_collection[painting] == 0:
				kol0 += 1
		
#Special cases 				
		if (my_collection[current_painting] >= 3):
			return 0
			
		if (my_collection[current_painting] == 0) and (kol0 == 1):
			return 0
		
#3 is achieved 
		# 3 3 0 0
		if (kol3 >= 2) and (my_collection[current_painting] == 0):
			return my_budget

		# 3 2 0 0
		if (kol3 >= 1) and (kol2 >= 1) and (my_collection[current_painting] == 0):
			return my_budget
		
		if (kol3 >= 1) and (kol2 >= 1) and (my_collection[current_painting] != 0):
			return 0			

		# 3 1 1 1/0		
		if (kol3 >= 1) and (kol2 == 0) and (kol1 >= 2) and (my_collection[current_painting] == 1):
			return my_budget
			
	
		if (kol3 >= 1) and (kol2 == 0) and (kol1 >= 2) and (my_collection[current_painting] == 0):
			return 0
		
#3 is not achieved 
		
		# 2 2 1 0
		if (kol3 == 0) and (kol2 >= 2) and ((kol1 >= 1) or (kol2 > 2)) and 	(my_collection[current_painting] == 2):
			return my_budget
		
		if (kol3 == 0) and (kol2 >= 2) and ((kol1 >= 1) or (kol2 > 2)) and (my_collection[current_painting] != 2):
			return 0
			
#amount of paintings requiered 
		arr = list(my_collection.values())
		arr.sort()
		needed_amount = max(1 - arr[1], 0) + max(2 - arr[2], 0) + max(3 - arr[3], 0)
# not special cases 		
		# 3 1 0 0 
		# 2 2 0 0 
		pred = 0
		for bot in bots:
			coll = bot['paintings']

			bkol3 = 0
			bkol2 = 0
			bkol1 = 0
			bkol0 = 0
			if (bot['budget'] == 0):
				pred = max(1, pred)
				continue
			
			for painting in coll:
				if coll[painting] >= 3:
					bkol3 += 1
				if coll[painting] == 2:
					bkol2 += 1
				if coll[painting] == 1:
					bkol1 += 1
				if coll[painting] == 0:
					bkol0 += 1
			
			if (coll[current_painting] >= 3):
				pred = max(0, pred)
				continue 
				
			
			# 3 3 0 0
			if (bkol3 >= 2) and (coll[current_painting] == 0):
				pred = max(bot['budget'], pred)
				continue
			
			
			if (coll[current_painting] == 0) and (bkol0 == 1):
				pred = max(0, pred)
				continue

			if (bkol3 >= 1) and (bkol2 >= 1) and (coll[current_painting] == 0):
				pred = max(bot['budget'], pred)
				continue
				
			if (bkol3 >= 1) and (bkol2 >= 1) and (coll[current_painting] != 0):
				pred = max(0, pred)
				continue
	
			if (bkol3 >= 1) and (bkol2 == 0) and (bkol1 >= 2) and (coll[current_painting] == 1):
				pred = max(bot['budget'], pred)
				continue
		
			if (bkol3 >= 1) and (bkol2 == 0) and (bkol1 >= 2) and (coll[current_painting] == 0):
				pred = max(0, pred)
				continue
				
			if (bkol3 == 0) and (bkol2 >= 2) and ((bkol1 >= 1) or (bkol2 > 2)) and (coll[current_painting] == 2):
				pred = max(bot['budget'], pred)
				continue
			
			if (bkol3 == 0) and (bkol2 >= 2) and ((bkol1 >= 1) or (bkol2 > 2)) and (coll[current_painting] != 2):
				pred = max(0, pred)
				continue
			
			barr = list(coll.values())
			barr.sort()
			bneeded_amount = max(1 - barr[1], 0) + max(2 - barr[2], 0) + max(3 - barr[3], 0)
			pred = max(pred, bot['budget']/bneeded_amount)
			
		pred = min(pred, my_budget/needed_amount)
		return pred

	def get_bid_game_type_value(self, current_round, bots, game_type, winner_pays, artists_and_values, round_limit,
		starting_budget, painting_order, target_collection, my_bot_details, current_painting, winner_ids, amounts_paid):
		"""Strategy for value type games.

		Parameters:
		current_round(int): 			The current round of the auction game
		bots(dict): 					A dictionary holding the details of all of the bots in the auction
										For each bot, you are given these details:
										bot_name(str):		The bot's name
										bot_unique_id(str):	A unique id for this bot
										paintings(dict):	A dict of the paintings won so far by this bot
										budget(int):		How much budget this bot has left
										score(int):			Current value of paintings (for value game)
		game_type(str): 				Will be either "collection" or "value", the two types of games we will play
		winner_pays(int):				Rank of bid that winner plays. 1 is 1st price auction. 2 is 2nd price auction.
		artists_and_values(dict):		A dictionary of the artist names and the painting value to the score (for value games)
		round_limit(int):				Total number of rounds in the game
		starting_budget(int):			How much budget each bot started with
		painting_order(list str):		A list of the full painting order
		target_collection(list int):	A list of the type of collection required to win, for collection games
										[5] means that you need 5 of any one type of painting
										[4,2] means you need 4 of one type of painting and 2 of another
										[3,2,1] means you need 3 of one type of painting, 2 of another, and 1 of another
		my_bot_details(dict):			Your bot details. Same as in the bots dict, but just your bot.
										Includes your current paintings, current score and current budget
		current_painting(str):			The artist of the current painting that is being bid on
		winner_ids(list str):			A list of the ids of the winners of each round so far
		amounts_paid(list int):			List of amounts paid for paintings in the rounds played so far

		Returns:
		int:Your bid. Return your bid for this round.
		"""
		# WRITE YOUR STRATEGY HERE FOR VALUE GAMES - MOST VALUABLE PAINTINGS WON WINS
		my_budget = my_bot_details["budget"]
		if (my_budget <= 1) or (current_round == 199):
			return my_budget
		
		overall = 0
		not_presented_yet = 0
		achieved_value = 0
		botswithoutmoney = 0
		
		#bots dont have money
		for bot in bots:
			if (bot['budget'] == 0):
				botswithoutmoney += 1
				
		if (botswithoutmoney == len(bots)-1):
			return 1
			
		#special case
		if (current_round <= 30):
			return 10
	
		for i in range(len(painting_order)):
			painting = painting_order[i]
			overall += artists_and_values[painting]
			if (i >= current_round):
				not_presented_yet += artists_and_values[painting]
		
		my_collection = my_bot_details["paintings"]
		for painting in my_collection:
			achieved_value += artists_and_values[painting] * my_collection[painting]

		if len(bots) == 2:
			special_coef = 1
			winningvalue = overall/2 + 1
		else:
			special_coef = 1+current_round/200
			winningvalue = overall/len(bots)*special_coef
			
		planned = not_presented_yet*special_coef/len(bots)
		
		bid = my_budget * artists_and_values[current_painting]/planned

		if achieved_value + not_presented_yet > winningvalue:
			bid *= special_coef

		if (current_painting == "Da Vinci") or (current_painting == "Rembrandt"):
			specialpred = my_budget*artists_and_values[current_painting]/not_presented_yet 
			return max(specialpred, bid)	

		return min(bid,my_budget)			
		

		
"""
		# Here is an example of how to get the current painting's value
		current_painting_value = artists_and_values[current_painting]
		print("The current painting's value is ", current_painting_value)

		# Here is an example of printing who won the last round
		if current_round>1:
			who_won_last_round = winner_ids[current_round-1]
			print("The last round was won by ", who_won_last_round)

		# Play around with printing out other variables in the function,
		# to see what kind of inputs you have to work with
		return random.randint(0, mymoney)
"""
