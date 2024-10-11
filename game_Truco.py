import random
import numpy as np

class Card:
    """
    Represents a card.

    Attributes:
        strDescriptor (str): String descriptor of the card.
        uid (int): Unique id of the card. Is the index that it takes when sorting the cards by string descriptor in increasing order.
        value (int): Number of card.
        suit (int): 0 = bastos, 1 = copas, 2 = espadas, 3 = oros.
        trucoValue (int): Strength of the card. Decides which card wins.
    """
    def __init__(self, strDescriptor: str, uid: int, value: int, suit: int, trucoValue: int):
        self.strDescriptor = strDescriptor
        self.uid = uid
        self.value = value
        self.suit = suit
        self.trucoValue = trucoValue

    def __str__(self):
        return f"{self.strDescriptor}"
    
class Hand:
    """
    Represents a hand.

    Attributes:
        C1 (Card): First card in the hand.
        C2 (Card): Second card in the hand.
        C3 (Card): Third card in the hand.
    """
    def __init__(self, C1: Card, C2: Card, C3: Card):
        self.cards = [C1, C2, C3]
        self.C1 = C1
        self.C2 = C2
        self.C3 = C3
        self.envidoValueOfHand, self.idexesOfCardsThatFormEnvidoValue = self.getEnvidoPointOfHand()

    def __getitem__(self, index: int):
        return self.cards[index]

    def __str__(self):
        return f"Cards: {self.C1} {self.C2} {self.C3} EnvidoValue: {self.envidoValueOfHand} CardIdxesThatFormEnvidoValue: {self.idexesOfCardsThatFormEnvidoValue}"

    def getEnvidoPointOfHand(self) -> tuple[int, tuple[int, int]]:
        """
        Returns envido point of the hand, and the two idx of the cards that form such envido point.

        Returns:
            (int, tuple[int, int]): Envido point of the hand, and tuple of two idx of the cards that form such envido point (if only one card defines envido value then it is repeated).
        """
        def getEnvidoValueOfCard(c: Card) -> int:
            if(c.value < 10):
                return c.value
            else:
                return 0
        
        def getEnvidoValueOfPairOfCards(c1: Card, c2: Card) -> int:
            if(c1.suit != c2.suit):
                envidoValueC1 = getEnvidoValueOfCard(c1)
                envidoValueC2 = getEnvidoValueOfCard(c2)

                return max(envidoValueC1, envidoValueC2)
            
            #Else cards share suit
            envidoValue = 20
            if(c1.value < 10): envidoValue += c1.value
            if(c2.value < 10): envidoValue += c2.value

            return envidoValue
        
        bestValueFound = -1
        idxC1 = -1
        idxC2 = -1

        for i in range(3):
            envidoValue = getEnvidoValueOfCard(self.cards[i])
            if(envidoValue > bestValueFound):
                bestValueFound = envidoValue
                idxC1 = i
                idxC2 = i

        for i in range(2):
            for j in range(i+1, 3):
                envidoValue = getEnvidoValueOfPairOfCards(self.cards[i], self.cards[j])
                if(envidoValue > bestValueFound):
                    bestValueFound = envidoValue
                    idxC1 = i
                    idxC2 = j

        return (bestValueFound, (idxC1, idxC2))

class Deck:
    cardsStr: list[str] = [
        "01b",
        "02b",
        "03b",
        "04b",
        "05b",
        "06b",
        "07b",
        "10b",
        "11b",
        "12b",
        
        "01c",
        "02c",
        "03c",
        "04c",
        "05c",
        "06c",
        "07c",
        "10c",
        "11c",
        "12c",

        "01e",
        "02e",
        "03e",
        "04e",
        "05e",
        "06e",
        "07e",
        "10e",
        "11e",
        "12e",

        "01o",
        "02o",
        "03o",
        "04o",
        "05o",
        "06o",
        "07o",
        "10o",
        "11o",
        "12o",
    ]

    cardIdByStr: dict[str, int] = {
        "01b": 0,
        "02b": 1,
        "03b": 2,
        "04b": 3,
        "05b": 4,
        "06b": 5,
        "07b": 6,
        "10b": 7,
        "11b": 8,
        "12b": 9,
        
        "01c": 10,
        "02c": 11,
        "03c": 12,
        "04c": 13,
        "05c": 14,
        "06c": 15,
        "07c": 16,
        "10c": 17,
        "11c": 18,
        "12c": 19,

        "01e": 20,
        "02e": 21,
        "03e": 22,
        "04e": 23,
        "05e": 24,
        "06e": 25,
        "07e": 26,
        "10e": 27,
        "11e": 28,
        "12e": 29,

        "01o": 30,
        "02o": 31,
        "03o": 32,
        "04o": 33,
        "05o": 34,
        "06o": 35,
        "07o": 36,
        "10o": 37,
        "11o": 38,
        "12o": 39,
    }

    cardValueByStr: dict[str, int] = {
        "01b": 1,
        "01c": 1,
        "01e": 1,
        "01o": 1,

        "02b": 2,
        "02c": 2,
        "02e": 2,
        "02o": 2,

        "03b": 3,
        "03c": 3,
        "03e": 3,
        "03o": 3,
        
        "04b": 4,
        "04c": 4,
        "04e": 4,
        "04o": 4,

        "05b": 5,
        "05c": 5,
        "05e": 5,
        "05o": 5,

        "06b": 6,
        "06c": 6,
        "06e": 6,
        "06o": 6,

        "07b": 7,
        "07c": 7,
        "07e": 7,
        "07o": 7,

        "10b": 10,
        "10c": 10,
        "10e": 10,
        "10o": 10,

        "11b": 11,
        "11c": 11,
        "11e": 11,
        "11o": 11,

        "12b": 12,
        "12c": 12,
        "12e": 12,
        "12o": 12,
    }

    cardTrucoValueByStr: dict[str, int] = {
        "04b": 0,
        "04c": 0,
        "04e": 0,
        "04o": 0,

        "05b": 1,
        "05c": 1,
        "05e": 1,
        "05o": 1,

        "06b": 2,
        "06c": 2,
        "06e": 2,
        "06o": 2,

        "07b": 3,
        "07c": 3,

        "10b": 4,
        "10c": 4,
        "10e": 4,
        "10o": 4,

        "11b": 5,
        "11c": 5,
        "11e": 5,
        "11o": 5,

        "12b": 6,
        "12c": 6,
        "12e": 6,
        "12o": 6,

        "01c": 7,
        "01o": 7,

        "02b": 8,
        "02c": 8,
        "02e": 8,
        "02o": 8,

        "03b": 9,
        "03c": 9,
        "03e": 9,
        "03o": 9,

        "07o": 10,
        
        "07e": 11,

        "01b": 12,

        "01e": 13
    }

    cardSuitByStr: dict[str, int] = {
        "01b": 0,
        "02b": 0,
        "03b": 0,
        "04b": 0,
        "05b": 0,
        "06b": 0,
        "07b": 0,
        "10b": 0,
        "11b": 0,
        "12b": 0,
        
        "01c": 1,
        "02c": 1,
        "03c": 1,
        "04c": 1,
        "05c": 1,
        "06c": 1,
        "07c": 1,
        "10c": 1,
        "11c": 1,
        "12c": 1,

        "01e": 2,
        "02e": 2,
        "03e": 2,
        "04e": 2,
        "05e": 2,
        "06e": 2,
        "07e": 2,
        "10e": 2,
        "11e": 2,
        "12e": 2,

        "01o": 3,
        "02o": 3,
        "03o": 3,
        "04o": 3,
        "05o": 3,
        "06o": 3,
        "07o": 3,
        "10o": 3,
        "11o": 3,
        "12o": 3,
    }
    
    def dealCards(self) -> tuple[Hand, Hand]:
        uids = random.sample(self.cardsStr, 6)
        cardsP1 = []
        cardsP2 = []
        for i in range(6):
            cardStr = uids[i]
            cardId = self.cardIdByStr[cardStr]
            cardValue = self.cardValueByStr[cardStr]
            cardSuit = self.cardSuitByStr[cardStr]
            cardTrucoValue = self.cardTrucoValueByStr[cardStr]

            if i <3:
                cardsP1.append(Card(cardStr, cardId, cardValue, cardSuit, cardTrucoValue))
            else: 
                cardsP2.append(Card(cardStr, cardId, cardValue, cardSuit, cardTrucoValue))
        
        return (Hand(cardsP1[0], cardsP1[1], cardsP1[2]), Hand(cardsP2[0], cardsP2[1], cardsP2[2]))


def trucoValueComparator(Card1: Card, Card2: Card):
    """
    Compares two cards by truco rank.

    Args:
        Card1 (Card): First card
        Card2 (Card): Second card

    Returns:
        int: [1: Card1 beats Card2, -1: Card1 loses to Card2, 0: draw]
    """

    if(Card1.trucoValue > Card2.trucoValue): return 1
    elif(Card1.trucoValue < Card2.trucoValue): return -1
    else: return 0

def envidoValueComparator(envValueP1: int, envValueP2: int):
    """
    Compares envido values.

    Args:
        envValueP1 (int): Envido value of player 1
        envValueP2 (int): Envido value of player 2

    Returns:
        int: [1: envValueP1 beats envValueP2, -1: envValueP1 loses to envValueP2, 0: draw]
    """
    if(envValueP1 > envValueP2): return 1
    elif(envValueP1 < envValueP2): return -1
    else: return 0


class Game:
    DECK = Deck()

    VALID_ENVIDO_BET_TRANSITIONS = {
        #[canSayEnvido, canSayRealEnvido, canSayFaltaEnvido]

        #sin canto
        0: [True, True, True],
        #envido
        2: [True, True, True],
        #realenvido
        3: [False, False, True],
        #envido envido
        4: [False, True, True],
        #envido realenvido
        5: [False, False, True],
        #envido envido realenvido
        7: [False, False, True],
    }

    stateSize = 655
    stateCartaSize = 58
    stateSelfEnvidoSize = 26
    stateCompartidoSize = 450
    stateTrucoBetHistorySize = 4
    stateEnvidoBetHistorySize = 5


    STATE_SECTIONS_INDECES = {
        "puntosTotalesP1": 0,
        "puntosTotalesP2": 1,
        "carta1": 2,
        "carta2": 2+stateCartaSize,
        "carta3": 2+stateCartaSize*2,
        "carta1EnMano": 2+stateCartaSize*3,
        "carta2EnMano": 2+stateCartaSize*3+1,
        "carta3EnMano": 2+stateCartaSize*3+2,
        "selfEnvidoSection": 2+stateCartaSize*3+3,
        "compartidoSection": 2+stateCartaSize*3+3+stateSelfEnvidoSize,
        "end": 2+stateCartaSize*3+3+stateSelfEnvidoSize+stateCompartidoSize
    }

    STATE_CARTAS_INDECES = {
        "absoluteId": 0,
        "cardRank": 40,
        "cardSuit": 54,
        "end": 58
    }

    STATE_SELF_ENVIDO_INDECES = {
        "puntos_int": 0,
        "puntos_id": 1,
        "carta1FormaEnvido": 23,
        "carta2FormaEnvido": 24,
        "carta3FormaEnvido": 25,
        "end": 26
    }

    STATE_COMPARTIDO_INDECES = {
        "isP1TrucoTurn": 0,
        "truco_P1HasToRespond": 1,
        "truco_P2HasToRespond": 2,
        "envido_P1HasToRespond": 3,
        "envido_P2HasToRespond": 4,
        "envidoAlreadyPlayed": 5,
        "carta1EnMesa": 6, #indicador de existencia
        "carta2EnMesa": 7,
        "carta3EnMesa": 8,
        "carta4EnMesa": 9,
        "carta5EnMesa": 10,
        "carta6EnMesa": 11,

        "carta1": 12,
        "carta2": 12+stateCartaSize,
        "carta3": 12+2*stateCartaSize,
        "carta4": 12+3*stateCartaSize,
        "carta5": 12+4*stateCartaSize,
        "carta6": 12+5*stateCartaSize,

        "trucoBetHistoryP1R1": 12+6*stateCartaSize,
        "trucoBetHistoryP1R2": 12+6*stateCartaSize+stateTrucoBetHistorySize,
        "trucoBetHistoryP1R3": 12+6*stateCartaSize+2*stateTrucoBetHistorySize,

        "trucoBetHistoryP2R1": 12+6*stateCartaSize+3*stateTrucoBetHistorySize,
        "trucoBetHistoryP2R2": 12+6*stateCartaSize+4*stateTrucoBetHistorySize,
        "trucoBetHistoryP2R3": 12+6*stateCartaSize+5*stateTrucoBetHistorySize,

        "trucoCanBetTrucoP1": 12+6*stateCartaSize+6*stateTrucoBetHistorySize,
        "trucoCanBetRetrucoP1": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+1,
        "trucoCanBetValecuatroP1": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+2,

        "trucoCanBetTrucoP2": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+3,
        "trucoCanBetRetrucoP2": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+4,
        "trucoCanBetValecuatroP2": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+5,

        "envidoBetHistoryP1": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+6,
        "envidoBetHistoryP2": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+6+stateEnvidoBetHistorySize,

        "envidoCanBetEnvidoP1": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+6+2*stateEnvidoBetHistorySize,
        "envidoCanBetRealEnvidoP1": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+6+2*stateEnvidoBetHistorySize+1,
        "envidoCanBetFaltaEnvidoP1": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+6+2*stateEnvidoBetHistorySize+2,

        "envidoCanBetEnvidoP2": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+6+2*stateEnvidoBetHistorySize+3,
        "envidoCanBetRealEnvidoP2": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+6+2*stateEnvidoBetHistorySize+4,
        "envidoCanBetFaltaEnvidoP2": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+6+2*stateEnvidoBetHistorySize+5,

        "envidoPuntosPublicosP1": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+6+2*stateEnvidoBetHistorySize+6,
        "envidoPuntosPublicosP2": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+6+2*stateEnvidoBetHistorySize+6+22,

        "end": 12+6*stateCartaSize+6*stateTrucoBetHistorySize+6+2*stateEnvidoBetHistorySize+6+2*22,
    }

    actionsSize = 11

    ACTION_INDECES = {
        "tirarC1": 0,
        "tirarC2": 1,
        "tirarC3": 2,
        "aceptarEnvidoBet": 3,
        "rechazarEnvidoBet": 4,
        "envido": 5,
        "realenvido": 6,
        "faltaenvido": 7,
        "aceptarTrucoBet": 8,
        "rechazarTrucoBet": 9,
        "betTruco": 10
    }

    ENVIDO_POINTS_INDECES = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 7,
        20: 8,
        21: 9,
        22: 10,
        23: 11,
        24: 12,
        25: 13,
        26: 14,
        27: 15,
        28: 16,
        29: 17,
        30: 18,
        31: 19,
        32: 20,
        33: 21
    }


    finalState = np.zeros(stateSize)
    
    def __init__(self):
        self.gameEnded = False
        self.puntosPartidaP1 = random.randint(0,29)
        self.puntosPartidaP2 = random.randint(0,29)
        self.resetRound()

    def resetRound(self):
        self.cartasEnMesa = [None, None, None, None, None, None]
        self.envido_puntosPublicosP1 = None
        self.envido_puntosPublicosP2 = None
        self.handP1, self.handP2 = self.DECK.dealCards()
        self.cardWasUsedP1 = [False, False, False]
        self.cardWasUsedP2 = [False, False, False]
        self.isP1Turn = True #defines who has to play
        self.isP1TrucoTurn = True #defines who has to throw a card
        self.currentRound = 0
        self.truco_puntosEnJuego = 1
        self.truco_P1CanBet = True
        self.truco_P2CanBet = True
        self.truco_P1HasToRespondBet = False
        self.truco_P2HasToRespondBet = False
        self.truco_roundsWonP1 = 0
        self.truco_roundsWonP2 = 0

        self.envido_puntosEnJuego = 0
        self.envido_puntosEnApuestaP1 = 0
        self.envido_puntosEnApuestaP2 = 0
        self.envido_P1CanBet = True
        self.envido_P2CanBet = True
        self.envido_P1HasToRespondBet = False
        self.envido_P2HasToRespondBet = False
        self.envido_P1ValidBets = [True,True,True]
        self.envido_P2ValidBets = [True,True,True]
        self.envido_faltaEnvidoWasChosen = False
        self.envido_alreadyPlayed = False

        self.action_reward_P1 = 0
        self.action_reward_P2 = 0

        self.initStates()

    def pasteCardState(self, card: Card, stateRef, startingIdx):
        if(card is None): return
        stateRef[startingIdx+self.STATE_CARTAS_INDECES["absoluteId"]+card.uid] = 1
        stateRef[startingIdx+self.STATE_CARTAS_INDECES["cardRank"]+card.trucoValue] = 1
        stateRef[startingIdx+self.STATE_CARTAS_INDECES["cardSuit"]+card.suit] = 1
    
    def initStates(self):
        self.stateP1 = np.zeros(self.stateSize)
        self.stateP2 = np.zeros(self.stateSize)

        self.stateP1[self.STATE_SECTIONS_INDECES["puntosTotalesP1"]] = self.puntosPartidaP1
        self.stateP2[self.STATE_SECTIONS_INDECES["puntosTotalesP1"]] = self.puntosPartidaP1

        self.stateP1[self.STATE_SECTIONS_INDECES["puntosTotalesP2"]] = self.puntosPartidaP2
        self.stateP2[self.STATE_SECTIONS_INDECES["puntosTotalesP2"]] = self.puntosPartidaP2

        self.pasteCardState(self.handP1[0], self.stateP1, self.STATE_SECTIONS_INDECES["carta1"])
        self.pasteCardState(self.handP1[1], self.stateP1, self.STATE_SECTIONS_INDECES["carta2"])
        self.pasteCardState(self.handP1[2], self.stateP1, self.STATE_SECTIONS_INDECES["carta3"])

        self.pasteCardState(self.handP2[0], self.stateP2, self.STATE_SECTIONS_INDECES["carta1"])
        self.pasteCardState(self.handP2[1], self.stateP2, self.STATE_SECTIONS_INDECES["carta2"])
        self.pasteCardState(self.handP2[2], self.stateP2, self.STATE_SECTIONS_INDECES["carta3"])

        self.stateP1[self.STATE_SECTIONS_INDECES["carta1EnMano"]] = 1
        self.stateP1[self.STATE_SECTIONS_INDECES["carta2EnMano"]] = 1
        self.stateP1[self.STATE_SECTIONS_INDECES["carta3EnMano"]] = 1

        self.stateP2[self.STATE_SECTIONS_INDECES["carta1EnMano"]] = 1
        self.stateP2[self.STATE_SECTIONS_INDECES["carta2EnMano"]] = 1
        self.stateP2[self.STATE_SECTIONS_INDECES["carta3EnMano"]] = 1


        #SelfEnvidoSection
        self.stateP1[
            self.STATE_SECTIONS_INDECES["selfEnvidoSection"] +
            self.STATE_SELF_ENVIDO_INDECES["puntos_int"]
            ] = self.handP1.envidoValueOfHand
        self.stateP1[
            self.STATE_SECTIONS_INDECES["selfEnvidoSection"] +
            self.STATE_SELF_ENVIDO_INDECES["puntos_id"] +
            self.ENVIDO_POINTS_INDECES[self.handP1.envidoValueOfHand]
            ] = 1
        self.stateP1[
            self.STATE_SECTIONS_INDECES["selfEnvidoSection"] +
            self.STATE_SELF_ENVIDO_INDECES["carta1FormaEnvido"] +
            self.handP1.idexesOfCardsThatFormEnvidoValue[0]
            ] = 1
        self.stateP1[
            self.STATE_SECTIONS_INDECES["selfEnvidoSection"] +
            self.STATE_SELF_ENVIDO_INDECES["carta1FormaEnvido"] +
            self.handP1.idexesOfCardsThatFormEnvidoValue[1]
            ] = 1
        
        self.stateP2[
            self.STATE_SECTIONS_INDECES["selfEnvidoSection"] +
            self.STATE_SELF_ENVIDO_INDECES["puntos_int"]
            ] = self.handP2.envidoValueOfHand
        self.stateP2[
            self.STATE_SECTIONS_INDECES["selfEnvidoSection"] +
            self.STATE_SELF_ENVIDO_INDECES["puntos_id"] +
            self.ENVIDO_POINTS_INDECES[self.handP2.envidoValueOfHand]
            ] = 1
        self.stateP2[
            self.STATE_SECTIONS_INDECES["selfEnvidoSection"] +
            self.STATE_SELF_ENVIDO_INDECES["carta1FormaEnvido"] +
            self.handP2.idexesOfCardsThatFormEnvidoValue[0]
            ] = 1
        self.stateP2[
            self.STATE_SECTIONS_INDECES["selfEnvidoSection"] +
            self.STATE_SELF_ENVIDO_INDECES["carta1FormaEnvido"] +
            self.handP2.idexesOfCardsThatFormEnvidoValue[1]
            ] = 1
        
        #Compartido
        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["isP1TrucoTurn"]
            ] = int(self.isP1TrucoTurn)
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["isP1TrucoTurn"]
            ] = int(self.isP1TrucoTurn)
        
        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["truco_P1HasToRespond"]
            ] = int(self.truco_P1HasToRespondBet)
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["truco_P1HasToRespond"]
            ] = int(self.truco_P1HasToRespondBet)
        
        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["truco_P2HasToRespond"]
            ] = int(self.truco_P2HasToRespondBet)
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["truco_P2HasToRespond"]
            ] = int(self.truco_P2HasToRespondBet)
        
        #Como no hay cartas indicadores de existencia de carta ya está en 0
        
        #Como no hay cartas en mesa no se inicializa

        #Como no hay jugadas entonces no hay historia

        if(self.truco_P1CanBet):
            if(self.truco_puntosEnJuego == 1):
                idx = 0
            elif(self.truco_puntosEnJuego == 2):
                idx = 1
            elif(self.truco_puntosEnJuego == 3):
                idx = 2
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP1"] +
                idx
                ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP1"] +
                idx
                ] = 1

        if(self.truco_P2CanBet):
            if(self.truco_puntosEnJuego == 1):
                idx = 0
            elif(self.truco_puntosEnJuego == 2):
                idx = 1
            elif(self.truco_puntosEnJuego == 3):
                idx = 2
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP2"] +
                idx
                ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP2"] +
                idx
                ] = 1
        

        self.refreshEnvidoState()
            
        #No hay puntos publicos
    
    def refreshEnvidoState(self):

        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envido_P1HasToRespond"]
            ] = int(self.envido_P1HasToRespondBet)
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envido_P1HasToRespond"]
            ] = int(self.envido_P1HasToRespondBet)
        
        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envido_P2HasToRespond"]
            ] = int(self.envido_P2HasToRespondBet)
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envido_P2HasToRespond"]
            ] = int(self.envido_P2HasToRespondBet)
        
        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoAlreadyPlayed"]
            ] = int(self.envido_alreadyPlayed)
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoAlreadyPlayed"]
            ] = int(self.envido_alreadyPlayed)
        
        
        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoCanBetEnvidoP1"]
            ] = int(self.envido_P1ValidBets[0])
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoCanBetEnvidoP1"]
            ] = int(self.envido_P1ValidBets[0])
            
        
        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoCanBetRealEnvidoP1"]
            ] = int(self.envido_P1ValidBets[1])
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoCanBetRealEnvidoP1"]
            ] = int(self.envido_P1ValidBets[1])
            
        
        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoCanBetFaltaEnvidoP1"]
            ] = int(self.envido_P1ValidBets[2])
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoCanBetFaltaEnvidoP1"]
            ] = int(self.envido_P1ValidBets[2])
            
        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoCanBetEnvidoP2"]
            ] = int(self.envido_P2ValidBets[0])
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoCanBetEnvidoP2"]
            ] = int(self.envido_P2ValidBets[0])
        
        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoCanBetRealEnvidoP2"]
            ] = int(self.envido_P2ValidBets[1])
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoCanBetRealEnvidoP2"]
            ] = int(self.envido_P2ValidBets[1])
            
        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoCanBetFaltaEnvidoP2"]
            ] = int(self.envido_P2ValidBets[2])
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["envidoCanBetFaltaEnvidoP2"]
            ] = int(self.envido_P2ValidBets[2])

        

    def getState(self):
        if(self.gameEnded): return self.finalState
        if(self.isP1Turn): return self.stateP1
        else: return self.stateP2


    def invalidActionFeedback(self):
        self.gameEnded = True
        if(self.isP1Turn): 
            self.action_reward_P1 -= 30
            self.action_reward_P2 -= 30
        else:
            self.action_reward_P1 += 30
            self.action_reward_P2 += 30 
        
        return False

    def throwCard(self, cardIdx):
        
        if(self.isP1Turn):
            #envido
            self.envido_P1CanBet = False
            self.envido_P1ValidBets = [False, False, False]
            self.refreshEnvidoState()

            #truco
            self.cartasEnMesa[2*self.currentRound] = self.handP1[cardIdx]
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"carta{2*self.currentRound+1}EnMesa"]
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"carta{2*self.currentRound+1}EnMesa"]
            ] = 1
            self.pasteCardState(self.handP1[cardIdx], self.stateP1, 
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"carta{2*self.currentRound+1}"]
            )
            self.pasteCardState(self.handP1[cardIdx], self.stateP2, 
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"carta{2*self.currentRound+1}"]
            )

            self.cardWasUsedP1[cardIdx] = True
            self.stateP1[
                self.STATE_SECTIONS_INDECES[f"carta{cardIdx+1}EnMano"]
            ] = 0

        else:
            #envido
            self.envido_P2CanBet = False
            self.envido_P2ValidBets = [False, False, False]
            self.refreshEnvidoState()

            #truco
            self.cartasEnMesa[2*self.currentRound+1] = self.handP2[cardIdx]
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"carta{2*self.currentRound+2}EnMesa"]
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"carta{2*self.currentRound+2}EnMesa"]
            ] = 1
            self.pasteCardState(self.handP2[cardIdx], self.stateP1, 
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"carta{2*self.currentRound+2}"]
            )
            self.pasteCardState(self.handP2[cardIdx], self.stateP2, 
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"carta{2*self.currentRound+2}"]
            )

            self.cardWasUsedP2[cardIdx] = True
            self.stateP2[
                self.STATE_SECTIONS_INDECES[f"carta{cardIdx+1}EnMano"]
            ] = 0

        self.isP1Turn = not self.isP1Turn
        self.isP1TrucoTurn = not self.isP1TrucoTurn

        if((self.cartasEnMesa[2*self.currentRound] is not None) and (self.cartasEnMesa[2*self.currentRound+1] is not None)):
            whoWon = trucoValueComparator(self.cartasEnMesa[2*self.currentRound], self.cartasEnMesa[2*self.currentRound+1])
            if(whoWon>=0):
                self.truco_roundsWonP1+=1
            if(whoWon<=0):
                self.truco_roundsWonP2+=1
            
            if(whoWon>=0):
                self.isP1TrucoTurn = True
                self.isP1Turn = True
            else:
                self.isP1TrucoTurn = False
                self.isP1Turn = False
            
            self.currentRound+=1

            #check if ended
            if(self.truco_roundsWonP1 == self.truco_roundsWonP2):
                if(self.truco_roundsWonP1==3 and self.truco_roundsWonP2==3):
                    self.action_reward_P1 += self.truco_puntosEnJuego
                    self.action_reward_P2 += self.truco_puntosEnJuego
                    self.gameEnded = True
            elif(self.truco_roundsWonP1>=2):
                self.action_reward_P1 += self.truco_puntosEnJuego
                self.action_reward_P2 += self.truco_puntosEnJuego
                self.gameEnded = True
            elif(self.truco_roundsWonP2>=2):
                self.action_reward_P1 += -self.truco_puntosEnJuego
                self.action_reward_P2 += -self.truco_puntosEnJuego
                self.gameEnded = True
        
        self.stateP1[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["isP1TrucoTurn"]
        ] = int(self.isP1TrucoTurn)
        self.stateP2[
            self.STATE_SECTIONS_INDECES["compartidoSection"] +
            self.STATE_COMPARTIDO_INDECES["isP1TrucoTurn"]
        ] = int(self.isP1TrucoTurn)


    def handleActionP1(self, action):

        if(action==0):
            #tirarC1
            if(not self.isP1TrucoTurn): return self.invalidActionFeedback()
            if(self.cardWasUsedP1[0]): return self.invalidActionFeedback()
            if(self.truco_P1HasToRespondBet): return self.invalidActionFeedback()
            if(self.envido_P1HasToRespondBet): return self.invalidActionFeedback()

            self.throwCard(0)

        if(action==1):
            #tirarC2
            if(not self.isP1TrucoTurn): return self.invalidActionFeedback()
            if(self.cardWasUsedP1[1]): return self.invalidActionFeedback()
            if(self.truco_P1HasToRespondBet): return self.invalidActionFeedback()
            if(self.envido_P1HasToRespondBet): return self.invalidActionFeedback()

            self.throwCard(1)
        
        if(action==2):
            #tirarC3
            if(not self.isP1TrucoTurn): return self.invalidActionFeedback()
            if(self.cardWasUsedP1[2]): return self.invalidActionFeedback()
            if(self.truco_P1HasToRespondBet): return self.invalidActionFeedback()
            if(self.envido_P1HasToRespondBet): return self.invalidActionFeedback()

            self.throwCard(2)
        
        if(action==3):
            #Acepta envido
            if(not self.envido_P1HasToRespondBet): return self.invalidActionFeedback()

            self.envido_puntosEnJuego = self.envido_puntosEnApuestaP2
            self.envido_alreadyPlayed = True
            self.envido_P1HasToRespondBet = False
            self.envido_P1CanBet = False
            self.envido_P2CanBet = False
            self.envido_P1ValidBets = [False, False, False]
            self.envido_P2ValidBets = [False, False, False]

            self.isP1Turn = self.isP1TrucoTurn
            if(self.truco_P1HasToRespondBet):
                self.isP1Turn = True
            if(self.truco_P2HasToRespondBet):
                self.isP1Turn = False

            if(self.handP1.envidoValueOfHand>=self.handP2.envidoValueOfHand):
                self.puntosPartidaP1 += self.envido_puntosEnJuego
                self.action_reward_P1 += self.envido_puntosEnJuego
                self.action_reward_P2 += self.envido_puntosEnJuego

                self.stateP1[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP1"] +
                    self.ENVIDO_POINTS_INDECES[self.handP1.envidoValueOfHand]
                ] = 1
                self.stateP2[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP1"] +
                    self.ENVIDO_POINTS_INDECES[self.handP1.envidoValueOfHand]
                ] = 1
            else:
                self.puntosPartidaP2 += self.envido_puntosEnJuego
                self.action_reward_P1 += -self.envido_puntosEnJuego
                self.action_reward_P2 += -self.envido_puntosEnJuego

                self.stateP1[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP1"] +
                    self.ENVIDO_POINTS_INDECES[self.handP1.envidoValueOfHand]
                ] = 1
                self.stateP2[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP1"] +
                    self.ENVIDO_POINTS_INDECES[self.handP1.envidoValueOfHand]
                ] = 1

                self.stateP1[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP2"] +
                    self.ENVIDO_POINTS_INDECES[self.handP2.envidoValueOfHand]
                ] = 1
                self.stateP2[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP2"] +
                    self.ENVIDO_POINTS_INDECES[self.handP2.envidoValueOfHand]
                ] = 1

            self.stateP1[self.STATE_SECTIONS_INDECES["puntosTotalesP1"]] = self.puntosPartidaP1
            self.stateP2[self.STATE_SECTIONS_INDECES["puntosTotalesP1"]] = self.puntosPartidaP1

            self.stateP1[self.STATE_SECTIONS_INDECES["puntosTotalesP2"]] = self.puntosPartidaP2
            self.stateP2[self.STATE_SECTIONS_INDECES["puntosTotalesP2"]] = self.puntosPartidaP2

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP1"] +
                3
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP1"] +
                3
            ] = 1
            self.refreshEnvidoState()

        if(action==4):
            #Rechaza envido
            if(not self.envido_P1HasToRespondBet): return self.invalidActionFeedback()

            self.envido_alreadyPlayed = True
            self.envido_P1HasToRespondBet = False
            self.envido_P1CanBet = False
            self.envido_P2CanBet = False
            self.envido_P1ValidBets = [False, False, False]
            self.envido_P2ValidBets = [False, False, False]

            self.puntosPartidaP2 += self.envido_puntosEnJuego
            self.action_reward_P1 -= self.envido_puntosEnJuego
            self.action_reward_P2 -= self.envido_puntosEnJuego

            self.isP1Turn = self.isP1TrucoTurn
            if(self.truco_P1HasToRespondBet):
                self.isP1Turn = True
            if(self.truco_P2HasToRespondBet):
                self.isP1Turn = False

            self.stateP1[self.STATE_SECTIONS_INDECES["puntosTotalesP1"]] = self.puntosPartidaP1
            self.stateP2[self.STATE_SECTIONS_INDECES["puntosTotalesP1"]] = self.puntosPartidaP1

            self.stateP1[self.STATE_SECTIONS_INDECES["puntosTotalesP2"]] = self.puntosPartidaP2
            self.stateP2[self.STATE_SECTIONS_INDECES["puntosTotalesP2"]] = self.puntosPartidaP2

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP1"] +
                4
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP1"] +
                4
            ] = 1
            self.refreshEnvidoState()

        if(action==5):
            #Envido
            if(self.envido_alreadyPlayed): return self.invalidActionFeedback()
            if(not self.envido_P1CanBet): return self.invalidActionFeedback()
            if(not self.envido_P1ValidBets[0]): return self.invalidActionFeedback()

            if(self.envido_puntosEnJuego==0):
                self.envido_puntosEnJuego=1
                self.envido_puntosEnApuestaP1 = 2
            elif(self.envido_P1HasToRespondBet):
                self.envido_puntosEnJuego=self.envido_puntosEnApuestaP2
                self.envido_puntosEnApuestaP1 = self.envido_puntosEnJuego + 2
            
            self.envido_P1HasToRespondBet = False
            self.envido_P2HasToRespondBet = True
            self.envido_P1CanBet = False
            self.envido_P2CanBet = True
            self.envido_P1ValidBets = [False, False, False]
            self.envido_P2ValidBets = self.VALID_ENVIDO_BET_TRANSITIONS[self.envido_puntosEnApuestaP1]

            self.isP1Turn = False

            #states
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP1"] +
                0
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP1"] +
                0
            ] = 1
            self.refreshEnvidoState()
        
        if(action==6):
            #RealEnvido
            if(self.envido_alreadyPlayed): return self.invalidActionFeedback()
            if(not self.envido_P1CanBet): return self.invalidActionFeedback()
            if(not self.envido_P1ValidBets[1]): return self.invalidActionFeedback()

            if(self.envido_puntosEnJuego==0):
                self.envido_puntosEnJuego=1
                self.envido_puntosEnApuestaP1 = 3
            elif(self.envido_P1HasToRespondBet):
                self.envido_puntosEnJuego=self.envido_puntosEnApuestaP2
                self.envido_puntosEnApuestaP1 = self.envido_puntosEnJuego + 3
            
            self.envido_P1HasToRespondBet = False
            self.envido_P2HasToRespondBet = True
            self.envido_P1CanBet = False
            self.envido_P2CanBet = True
            self.envido_P1ValidBets = [False, False, False]
            self.envido_P2ValidBets = self.VALID_ENVIDO_BET_TRANSITIONS[self.envido_puntosEnApuestaP1]

            self.isP1Turn = False

            #states
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP1"] +
                1
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP1"] +
                1
            ] = 1
            self.refreshEnvidoState()

        if(action==7):
            #FaltaEnvido
            if(self.envido_alreadyPlayed): return self.invalidActionFeedback()
            if(not self.envido_P1CanBet): return self.invalidActionFeedback()
            if(not self.envido_P1ValidBets[2]): return self.invalidActionFeedback()

            self.envido_faltaEnvidoWasChosen = True
            if(self.envido_puntosEnJuego==0):
                self.envido_puntosEnJuego=1
            elif(self.envido_P1HasToRespondBet):
                self.envido_puntosEnJuego=self.envido_puntosEnApuestaP2

            self.envido_puntosEnApuestaP1 = min(30-self.puntosPartidaP1, 30-self.puntosPartidaP2)
            
            self.envido_P1HasToRespondBet = False
            self.envido_P2HasToRespondBet = True
            self.envido_P1CanBet = False
            self.envido_P2CanBet = False
            self.envido_P1ValidBets = [False, False, False]
            self.envido_P2ValidBets = [False, False, False]

            self.isP1Turn = False

            #states
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP1"] +
                2
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP1"] +
                2
            ] = 1
            self.refreshEnvidoState()

        if(action == 8):
            #aceptar Truco bet
            if(self.envido_P1HasToRespondBet): return self.invalidActionFeedback()
            if(not self.truco_P1HasToRespondBet): return self.invalidActionFeedback()

            self.envido_P1ValidBets = [False, False, False]
            self.refreshEnvidoState()

            self.truco_puntosEnJuego += 1
            self.isP1Turn = self.isP1TrucoTurn
            
            self.truco_P1HasToRespondBet = False
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["truco_P1HasToRespond"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["truco_P1HasToRespond"]
            ] = 0

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"trucoBetHistoryP1R{self.currentRound+1}"] +
                3
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"trucoBetHistoryP1R{self.currentRound+1}"] +
                3
            ] = 1

        if(action == 9):
            #Rechazar truco bet
            if(self.envido_P1HasToRespondBet): return self.invalidActionFeedback()
            if(not self.truco_P1HasToRespondBet): return self.invalidActionFeedback()
            
            self.gameEnded = True
            self.action_reward_P1 -= self.truco_puntosEnJuego
            self.action_reward_P2 -= self.truco_puntosEnJuego
     
        if(action == 10):
            #bet Truco
            if(not self.truco_P1CanBet): return self.invalidActionFeedback()
            if(self.envido_P1HasToRespondBet): return self.invalidActionFeedback()
            

            self.envido_P1ValidBets = [False, False, False]
            self.refreshEnvidoState()

            if(self.truco_P1HasToRespondBet):
                self.truco_puntosEnJuego += 1
            self.isP1Turn = False
            self.truco_P1CanBet = False
            if(self.truco_puntosEnJuego!=3):
                self.truco_P2CanBet = True
            self.truco_P1HasToRespondBet = False
            self.truco_P2HasToRespondBet = True

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["truco_P1HasToRespond"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["truco_P1HasToRespond"]
            ] = 0

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["truco_P2HasToRespond"]
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["truco_P2HasToRespond"]
            ] = 1

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"trucoBetHistoryP1R{self.currentRound+1}"] +
                self.truco_puntosEnJuego-1
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"trucoBetHistoryP1R{self.currentRound+1}"] +
                self.truco_puntosEnJuego-1
            ] = 1

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP1"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP1"]
            ] = 0
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP1"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP1"]
            ] = 0
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP1"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP1"]
            ] = 0

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP2"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP2"]
            ] = 0
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP2"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP2"]
            ] = 0
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP2"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP2"]
            ] = 0

            if(self.truco_puntosEnJuego==1):
                self.stateP1[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP2"]
                ] = 1
                self.stateP2[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP2"]
                ] = 1
            elif(self.truco_puntosEnJuego==2):
                self.stateP1[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP2"]
                ] = 1
                self.stateP2[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP2"]
                ] = 1


    def handleActionP2(self, action):
        if(action==0):
            #tirarC1
            if(self.isP1TrucoTurn): return self.invalidActionFeedback()
            if(self.cardWasUsedP2[0]): return self.invalidActionFeedback()
            if(self.truco_P2HasToRespondBet): return self.invalidActionFeedback()
            if(self.envido_P2HasToRespondBet): return self.invalidActionFeedback()

            self.throwCard(0)

        if(action==1):
            #tirarC2
            if(self.isP1TrucoTurn): return self.invalidActionFeedback()
            if(self.cardWasUsedP2[1]): return self.invalidActionFeedback()
            if(self.truco_P2HasToRespondBet): return self.invalidActionFeedback()
            if(self.envido_P2HasToRespondBet): return self.invalidActionFeedback()

            self.throwCard(1)
        
        if(action==2):
            #tirarC3
            if(self.isP1TrucoTurn): return self.invalidActionFeedback()
            if(self.cardWasUsedP2[2]): return self.invalidActionFeedback()
            if(self.truco_P2HasToRespondBet): return self.invalidActionFeedback()
            if(self.envido_P2HasToRespondBet): return self.invalidActionFeedback()

            self.throwCard(2)

        if(action==3):
            #Acepta envido
            if(not self.envido_P2HasToRespondBet): return self.invalidActionFeedback()

            self.envido_puntosEnJuego = self.envido_puntosEnApuestaP1
            self.envido_alreadyPlayed = True
            self.envido_P2HasToRespondBet = False
            self.envido_P1CanBet = False
            self.envido_P2CanBet = False
            self.envido_P1ValidBets = [False, False, False]
            self.envido_P2ValidBets = [False, False, False]

            self.isP1Turn = self.isP1TrucoTurn

            if(self.truco_P1HasToRespondBet):
                self.isP1Turn = True
            if(self.truco_P2HasToRespondBet):
                self.isP1Turn = False

            if(self.handP1.envidoValueOfHand>=self.handP2.envidoValueOfHand):
                self.puntosPartidaP1 += self.envido_puntosEnJuego
                self.action_reward_P1 += self.envido_puntosEnJuego
                self.action_reward_P2 += self.envido_puntosEnJuego

                self.stateP1[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP1"] +
                    self.ENVIDO_POINTS_INDECES[self.handP1.envidoValueOfHand]
                ] = 1
                self.stateP2[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP1"] +
                    self.ENVIDO_POINTS_INDECES[self.handP1.envidoValueOfHand]
                ] = 1
            else:
                self.puntosPartidaP2 += self.envido_puntosEnJuego
                self.action_reward_P1 += -self.envido_puntosEnJuego
                self.action_reward_P2 += -self.envido_puntosEnJuego

                self.stateP1[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP1"] +
                    self.ENVIDO_POINTS_INDECES[self.handP1.envidoValueOfHand]
                ] = 1
                self.stateP2[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP1"] +
                    self.ENVIDO_POINTS_INDECES[self.handP1.envidoValueOfHand]
                ] = 1

                self.stateP1[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP2"] +
                    self.ENVIDO_POINTS_INDECES[self.handP2.envidoValueOfHand]
                ] = 1
                self.stateP2[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP2"] +
                    self.ENVIDO_POINTS_INDECES[self.handP2.envidoValueOfHand]
                ] = 1

            self.stateP1[self.STATE_SECTIONS_INDECES["puntosTotalesP1"]] = self.puntosPartidaP1
            self.stateP2[self.STATE_SECTIONS_INDECES["puntosTotalesP1"]] = self.puntosPartidaP1

            self.stateP1[self.STATE_SECTIONS_INDECES["puntosTotalesP2"]] = self.puntosPartidaP2
            self.stateP2[self.STATE_SECTIONS_INDECES["puntosTotalesP2"]] = self.puntosPartidaP2

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP2"] +
                3
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP2"] +
                3
            ] = 1
            self.refreshEnvidoState()
        
        if(action==4):
            #Rechaza envido
            if(not self.envido_P2HasToRespondBet): return self.invalidActionFeedback()

            self.envido_alreadyPlayed = True
            self.envido_P2HasToRespondBet = False
            self.envido_P1CanBet = False
            self.envido_P2CanBet = False
            self.envido_P1ValidBets = [False, False, False]
            self.envido_P2ValidBets = [False, False, False]

            self.puntosPartidaP1 += self.envido_puntosEnJuego
            self.action_reward_P1 += self.envido_puntosEnJuego
            self.action_reward_P2 += self.envido_puntosEnJuego

            self.isP1Turn = self.isP1TrucoTurn
            if(self.truco_P1HasToRespondBet):
                self.isP1Turn = True
            if(self.truco_P2HasToRespondBet):
                self.isP1Turn = False

            self.stateP1[self.STATE_SECTIONS_INDECES["puntosTotalesP1"]] = self.puntosPartidaP1
            self.stateP2[self.STATE_SECTIONS_INDECES["puntosTotalesP1"]] = self.puntosPartidaP1

            self.stateP1[self.STATE_SECTIONS_INDECES["puntosTotalesP2"]] = self.puntosPartidaP2
            self.stateP2[self.STATE_SECTIONS_INDECES["puntosTotalesP2"]] = self.puntosPartidaP2

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP2"] +
                4
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP2"] +
                4
            ] = 1
            self.refreshEnvidoState()

        if(action==5):
            #Envido
            if(self.envido_alreadyPlayed): return self.invalidActionFeedback()
            if(not self.envido_P2CanBet): return self.invalidActionFeedback()
            if(not self.envido_P2ValidBets[0]): return self.invalidActionFeedback()

            if(self.envido_puntosEnJuego==0):
                self.envido_puntosEnJuego=1
                self.envido_puntosEnApuestaP2 = 2
            elif(self.envido_P2HasToRespondBet):
                self.envido_puntosEnJuego=self.envido_puntosEnApuestaP1
                self.envido_puntosEnApuestaP2 = self.envido_puntosEnJuego + 2
            
            self.envido_P2HasToRespondBet = False
            self.envido_P1HasToRespondBet = True
            self.envido_P2CanBet = False
            self.envido_P1CanBet = True
            self.envido_P2ValidBets = [False, False, False]
            self.envido_P1ValidBets = self.VALID_ENVIDO_BET_TRANSITIONS[self.envido_puntosEnApuestaP2]

            self.isP1Turn = True

            #states
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP2"] +
                0
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP2"] +
                0
            ] = 1
            self.refreshEnvidoState()
        
        if(action==6):
            #RealEnvido
            if(self.envido_alreadyPlayed): return self.invalidActionFeedback()
            if(not self.envido_P2CanBet): return self.invalidActionFeedback()
            if(not self.envido_P2ValidBets[1]): return self.invalidActionFeedback()

            if(self.envido_puntosEnJuego==0):
                self.envido_puntosEnJuego=1
                self.envido_puntosEnApuestaP2 = 3
            elif(self.envido_P2HasToRespondBet):
                self.envido_puntosEnJuego=self.envido_puntosEnApuestaP1
                self.envido_puntosEnApuestaP2 = self.envido_puntosEnJuego + 3
            
            self.envido_P2HasToRespondBet = False
            self.envido_P1HasToRespondBet = True
            self.envido_P2CanBet = False
            self.envido_P1CanBet = True
            self.envido_P2ValidBets = [False, False, False]
            self.envido_P1ValidBets = self.VALID_ENVIDO_BET_TRANSITIONS[self.envido_puntosEnApuestaP2]

            self.isP1Turn = True

            #states
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP2"] +
                1
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP2"] +
                1
            ] = 1
            self.refreshEnvidoState()

        if(action==7):
            #FaltaEnvido
            if(self.envido_alreadyPlayed): return self.invalidActionFeedback()
            if(not self.envido_P2CanBet): return self.invalidActionFeedback()
            if(not self.envido_P2ValidBets[2]): return self.invalidActionFeedback()

            self.envido_faltaEnvidoWasChosen = True
            if(self.envido_puntosEnJuego==0):
                self.envido_puntosEnJuego=1
            elif(self.envido_P2HasToRespondBet):
                self.envido_puntosEnJuego=self.envido_puntosEnApuestaP1

            self.envido_puntosEnApuestaP2 = min(30-self.puntosPartidaP1, 30-self.puntosPartidaP2)
            
            self.envido_P2HasToRespondBet = False
            self.envido_P1HasToRespondBet = True
            self.envido_P2CanBet = False
            self.envido_P1CanBet = False
            self.envido_P1ValidBets = [False, False, False]
            self.envido_P2ValidBets = [False, False, False]

            self.isP1Turn = True

            #states
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP2"] +
                2
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP2"] +
                2
            ] = 1
            self.refreshEnvidoState()
        
        if(action == 8):
            #aceptar Truco bet
            if(self.envido_P2HasToRespondBet): return self.invalidActionFeedback()
            if(not self.truco_P2HasToRespondBet): return self.invalidActionFeedback()

            self.envido_P2ValidBets = [False, False, False]
            self.refreshEnvidoState()

            self.truco_puntosEnJuego += 1
            self.isP1Turn = self.isP1TrucoTurn
            
            self.truco_P2HasToRespondBet = False
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["truco_P2HasToRespond"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["truco_P2HasToRespond"]
            ] = 0

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"trucoBetHistoryP2R{self.currentRound+1}"] +
                3
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"trucoBetHistoryP2R{self.currentRound+1}"] +
                3
            ] = 1

        if(action == 9):
            #Rechazar truco bet
            if(self.envido_P2HasToRespondBet): return self.invalidActionFeedback()
            if(not self.truco_P2HasToRespondBet): return self.invalidActionFeedback()
            
            self.gameEnded = True
            self.action_reward_P1 += self.truco_puntosEnJuego
            self.action_reward_P2 += self.truco_puntosEnJuego
       
        if(action == 10):
            #bet Truco
            if(not self.truco_P2CanBet): return self.invalidActionFeedback()
            if(self.envido_P2HasToRespondBet): return self.invalidActionFeedback()
            

            if(self.truco_P2HasToRespondBet):
                self.truco_puntosEnJuego += 1
            self.isP1Turn = True
            self.truco_P2CanBet = False
            if(self.truco_puntosEnJuego!=3):
                self.truco_P1CanBet = True
            self.truco_P2HasToRespondBet = False
            self.truco_P1HasToRespondBet = True

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["truco_P2HasToRespond"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["truco_P2HasToRespond"]
            ] = 0

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["truco_P1HasToRespond"]
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["truco_P1HasToRespond"]
            ] = 1

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"trucoBetHistoryP2R{self.currentRound+1}"] +
                self.truco_puntosEnJuego-1
            ] = 1
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES[f"trucoBetHistoryP2R{self.currentRound+1}"] +
                self.truco_puntosEnJuego-1
            ] = 1

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP2"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP2"]
            ] = 0
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP2"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP2"]
            ] = 0
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP2"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP2"]
            ] = 0

            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP2"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP2"]
            ] = 0
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP2"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP2"]
            ] = 0
            self.stateP1[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP2"]
            ] = 0
            self.stateP2[
                self.STATE_SECTIONS_INDECES["compartidoSection"] +
                self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP2"]
            ] = 0

            if(self.truco_puntosEnJuego==1):
                self.stateP1[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP1"]
                ] = 1
                self.stateP2[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP1"]
                ] = 1
            elif(self.truco_puntosEnJuego==2):
                self.stateP1[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP1"]
                ] = 1
                self.stateP2[
                    self.STATE_SECTIONS_INDECES["compartidoSection"] +
                    self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP1"]
                ] = 1

            self.envido_P2ValidBets = [False, False, False]
            self.refreshEnvidoState()

    def step(self, action):
        #action
        #[tirarC1, tirarC2, tirarC3, aceptarEnvidoBet, envido, realenvido, faltaenvido, aceptarTrucoBet, betTruco]
        if(self.isP1Turn):
            self.action_reward_P1 = 0
            self.handleActionP1(action)
        else:
            self.action_reward_P2 = 0
            self.handleActionP2(action)

        if(self.puntosPartidaP1>=30):
            self.gameEnded = True
            self.action_reward_P1 += 30
            self.action_reward_P2 += 30

        if(self.puntosPartidaP2>=30):
            self.gameEnded = True
            self.action_reward_P1 -= 30
            self.action_reward_P2 -= 30

        if(self.isP1Turn):
            return (self.getState(), self.action_reward_P1, self.gameEnded)
        else:
            return (self.getState(), self.action_reward_P2, self.gameEnded)
            
        
    
    def gameFinished(self):
        return self.gameEnded
    
    def getIsP1Turn(self):
        return self.isP1Turn
    
    def printStateP1(self):
        print("//////////////")
        print("State P1")
        
        print("+++++++++++")
        print(f"Puntos partida ({self.stateP1[self.STATE_SECTIONS_INDECES['puntosTotalesP1']]} - {self.stateP1[self.STATE_SECTIONS_INDECES['puntosTotalesP2']]})")
        
        print("+++++++++++")
        print(f"Carta1 (enMano = {self.stateP1[self.STATE_SECTIONS_INDECES['carta1EnMano']]})")
        idxCarta = self.STATE_SECTIONS_INDECES["carta1"]
        print("Carta1 id:", self.stateP1[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta1 rank:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta1 suit:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])
        
        
        print("+++++++++++")
        print(f"Carta2 (enMano = {self.stateP1[self.STATE_SECTIONS_INDECES['carta2EnMano']]})")
        idxCarta = self.STATE_SECTIONS_INDECES["carta2"]
        print("Carta2 id:", self.stateP1[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta2 rank:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta2 suit:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])
        
        print("+++++++++++")
        print(f"Carta3 (enMano = {self.stateP1[self.STATE_SECTIONS_INDECES['carta3EnMano']]})")
        idxCarta = self.STATE_SECTIONS_INDECES["carta3"]
        print("Carta3 id:", self.stateP1[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta3 rank:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta3 suit:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])

        print("+++++++++++")
        envSectionIdx = self.STATE_SECTIONS_INDECES["selfEnvidoSection"]
        print(f"Puntos envido: {self.stateP1[envSectionIdx + self.STATE_SELF_ENVIDO_INDECES['puntos_int']]}")
        print("Puntos envido id", self.stateP1[envSectionIdx + self.STATE_SELF_ENVIDO_INDECES['puntos_id']:envSectionIdx + self.STATE_SELF_ENVIDO_INDECES['carta1FormaEnvido']])
        print(f"Cartas que forman envido: ({self.stateP1[envSectionIdx + self.STATE_SELF_ENVIDO_INDECES['carta1FormaEnvido']]} {self.stateP1[envSectionIdx + self.STATE_SELF_ENVIDO_INDECES['carta2FormaEnvido']]} {self.stateP1[envSectionIdx + self.STATE_SELF_ENVIDO_INDECES['carta3FormaEnvido']]})")


        print("+++++++++++")
        print("COMPARTIDO")
        print(f"isP1TrucoTurn:", self.stateP1[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["isP1TrucoTurn"]])
        print(f"truco_P1HasToRespond:", self.stateP1[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["truco_P1HasToRespond"]])
        print(f"truco_P2HasToRespond:", self.stateP1[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["truco_P2HasToRespond"]])
        print(f"envido_P1HasToRespond:", self.stateP1[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envido_P1HasToRespond"]])
        print(f"envido_P2HasToRespond:", self.stateP1[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envido_P2HasToRespond"]])
        print(f"envidoAlreadyPlayed:", self.stateP1[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoAlreadyPlayed"]])
        print(f"carta1EnMesa:", self.stateP1[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta1EnMesa"]])
        print(f"carta2EnMesa:", self.stateP1[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta2EnMesa"]])
        print(f"carta3EnMesa:", self.stateP1[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta3EnMesa"]])
        print(f"carta4EnMesa:", self.stateP1[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta4EnMesa"]])
        print(f"carta5EnMesa:", self.stateP1[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta5EnMesa"]])
        print(f"carta6EnMesa:", self.stateP1[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta6EnMesa"]])

        print("+++++++++++")
        print("Carta1 Mesa")
        idxCarta = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta1"]
        print("Carta1 id:", self.stateP1[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta1 rank:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta1 suit:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])

        print("+++++++++++")
        print(f"Carta2 Mesa")
        idxCarta = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta2"]
        print("Carta2 id:", self.stateP1[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta2 rank:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta2 suit:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])

        print("+++++++++++")
        print(f"Carta3 Mesa")
        idxCarta = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta3"]
        print("Carta3 id:", self.stateP1[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta3 rank:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta3 suit:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])

        print("+++++++++++")
        print(f"Carta4 Mesa")
        idxCarta = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta4"]
        print("Carta4 id:", self.stateP1[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta4 rank:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta4 suit:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])

        print("+++++++++++")
        print(f"Carta5 Mesa")
        idxCarta = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta5"]
        print("Carta5 id:", self.stateP1[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta5 rank:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta5 suit:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])

        print("+++++++++++")
        print(f"Carta6 Mesa")
        idxCarta = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta6"]
        print("Carta6 id:", self.stateP1[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta6 rank:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta6 suit:", self.stateP1[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])
        
        print("+++++++++++")
        print("Truco Betting History")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoBetHistoryP1R1"]
        print("P1R1:",self.stateP1[idx:idx+self.stateTrucoBetHistorySize])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoBetHistoryP1R2"]
        print("P1R2:",self.stateP1[idx:idx+self.stateTrucoBetHistorySize])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoBetHistoryP1R3"]
        print("P1R3:",self.stateP1[idx:idx+self.stateTrucoBetHistorySize])

        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoBetHistoryP2R1"]
        print("P2R1:",self.stateP1[idx:idx+self.stateTrucoBetHistorySize])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoBetHistoryP2R2"]
        print("P2R2:",self.stateP1[idx:idx+self.stateTrucoBetHistorySize])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoBetHistoryP2R3"]
        print("P2R3:",self.stateP1[idx:idx+self.stateTrucoBetHistorySize])

        print("+++++++++++")
        print("P1 Valid truco bets")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP1"]
        print("Can bet truco:", self.stateP1[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP1"]
        print("Can bet retruco:", self.stateP1[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP1"]
        print("Can bet valecuatro:", self.stateP1[idx])

        print("P2 Valid truco bets")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP2"]
        print("Can bet truco:", self.stateP1[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP2"]
        print("Can bet retruco:", self.stateP1[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP2"]
        print("Can bet valecuatro:", self.stateP1[idx])

        print("+++++++++++")
        print("Envido Betting History")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP1"]
        print("P1:",self.stateP1[idx:idx+self.stateEnvidoBetHistorySize])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP2"]
        print("P2:",self.stateP1[idx:idx+self.stateEnvidoBetHistorySize])

        print("+++++++++++")
        print("P1 Valid envido bets")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoCanBetEnvidoP1"]
        print("Can bet envido:", self.stateP1[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoCanBetRealEnvidoP1"]
        print("Can bet realenvido:", self.stateP1[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoCanBetFaltaEnvidoP1"]
        print("Can bet faltaenvido:", self.stateP1[idx])

        print("P2 Valid envido bets")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoCanBetEnvidoP2"]
        print("Can bet envido:", self.stateP1[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoCanBetRealEnvidoP2"]
        print("Can bet realenvido:", self.stateP1[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoCanBetFaltaEnvidoP2"]
        print("Can bet faltaenvido:", self.stateP1[idx])

        print("+++++++++++")
        print("Puntos publicos P1")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP1"]
        print(self.stateP1[idx:idx+22])
        print("Puntos publicos P2")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP2"]
        print(self.stateP1[idx:idx+22])

        print("/////////////////////////")
    
    def printStateP2(self):
        print("//////////////")
        print("State P2")
        
        print("+++++++++++")
        print(f"Puntos partida ({self.stateP2[self.STATE_SECTIONS_INDECES['puntosTotalesP1']]} - {self.stateP2[self.STATE_SECTIONS_INDECES['puntosTotalesP2']]})")
        
        print("+++++++++++")
        print(f"Carta1 (enMano = {self.stateP2[self.STATE_SECTIONS_INDECES['carta1EnMano']]})")
        idxCarta = self.STATE_SECTIONS_INDECES["carta1"]
        print("Carta1 id:", self.stateP2[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta1 rank:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta1 suit:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])
        
        
        print("+++++++++++")
        print(f"Carta2 (enMano = {self.stateP2[self.STATE_SECTIONS_INDECES['carta2EnMano']]})")
        idxCarta = self.STATE_SECTIONS_INDECES["carta2"]
        print("Carta2 id:", self.stateP2[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta2 rank:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta2 suit:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])
        
        print("+++++++++++")
        print(f"Carta3 (enMano = {self.stateP2[self.STATE_SECTIONS_INDECES['carta3EnMano']]})")
        idxCarta = self.STATE_SECTIONS_INDECES["carta3"]
        print("Carta3 id:", self.stateP2[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta3 rank:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta3 suit:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])

        print("+++++++++++")
        envSectionIdx = self.STATE_SECTIONS_INDECES["selfEnvidoSection"]
        print(f"Puntos envido: {self.stateP2[envSectionIdx + self.STATE_SELF_ENVIDO_INDECES['puntos_int']]}")
        print("Puntos envido id", self.stateP2[envSectionIdx + self.STATE_SELF_ENVIDO_INDECES['puntos_id']:envSectionIdx + self.STATE_SELF_ENVIDO_INDECES['carta1FormaEnvido']])
        print(f"Cartas que forman envido: ({self.stateP2[envSectionIdx + self.STATE_SELF_ENVIDO_INDECES['carta1FormaEnvido']]} {self.stateP2[envSectionIdx + self.STATE_SELF_ENVIDO_INDECES['carta2FormaEnvido']]} {self.stateP2[envSectionIdx + self.STATE_SELF_ENVIDO_INDECES['carta3FormaEnvido']]})")


        print("+++++++++++")
        print("COMPARTIDO")
        print(f"isP1TrucoTurn:", self.stateP2[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["isP1TrucoTurn"]])
        print(f"truco_P1HasToRespond:", self.stateP2[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["truco_P1HasToRespond"]])
        print(f"truco_P2HasToRespond:", self.stateP2[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["truco_P2HasToRespond"]])
        print(f"envido_P1HasToRespond:", self.stateP2[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envido_P1HasToRespond"]])
        print(f"envido_P2HasToRespond:", self.stateP2[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envido_P2HasToRespond"]])
        print(f"envidoAlreadyPlayed:", self.stateP2[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoAlreadyPlayed"]])
        print(f"carta1EnMesa:", self.stateP2[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta1EnMesa"]])
        print(f"carta2EnMesa:", self.stateP2[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta2EnMesa"]])
        print(f"carta3EnMesa:", self.stateP2[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta3EnMesa"]])
        print(f"carta4EnMesa:", self.stateP2[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta4EnMesa"]])
        print(f"carta5EnMesa:", self.stateP2[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta5EnMesa"]])
        print(f"carta6EnMesa:", self.stateP2[self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta6EnMesa"]])

        print("+++++++++++")
        print("Carta1 Mesa")
        idxCarta = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta1"]
        print("Carta1 id:", self.stateP2[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta1 rank:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta1 suit:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])

        print("+++++++++++")
        print(f"Carta2 Mesa")
        idxCarta = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta2"]
        print("Carta2 id:", self.stateP2[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta2 rank:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta2 suit:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])

        print("+++++++++++")
        print(f"Carta3 Mesa")
        idxCarta = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta3"]
        print("Carta3 id:", self.stateP2[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta3 rank:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta3 suit:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])

        print("+++++++++++")
        print(f"Carta4 Mesa")
        idxCarta = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta4"]
        print("Carta4 id:", self.stateP2[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta4 rank:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta4 suit:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])

        print("+++++++++++")
        print(f"Carta5 Mesa")
        idxCarta = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta5"]
        print("Carta5 id:", self.stateP2[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta5 rank:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta5 suit:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])

        print("+++++++++++")
        print(f"Carta6 Mesa")
        idxCarta = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["carta6"]
        print("Carta6 id:", self.stateP2[idxCarta:idxCarta+self.STATE_CARTAS_INDECES["cardRank"]])
        print("Carta6 rank:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardRank"]:idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]])
        print("Carta6 suit:", self.stateP2[idxCarta+self.STATE_CARTAS_INDECES["cardSuit"]:idxCarta+self.STATE_CARTAS_INDECES["end"]])
        
        print("+++++++++++")
        print("Truco Betting History")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoBetHistoryP1R1"]
        print("P1R1:",self.stateP2[idx:idx+self.stateTrucoBetHistorySize])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoBetHistoryP1R2"]
        print("P1R2:",self.stateP2[idx:idx+self.stateTrucoBetHistorySize])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoBetHistoryP1R3"]
        print("P1R3:",self.stateP2[idx:idx+self.stateTrucoBetHistorySize])

        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoBetHistoryP2R1"]
        print("P2R1:",self.stateP2[idx:idx+self.stateTrucoBetHistorySize])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoBetHistoryP2R2"]
        print("P2R2:",self.stateP2[idx:idx+self.stateTrucoBetHistorySize])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoBetHistoryP2R3"]
        print("P2R3:",self.stateP2[idx:idx+self.stateTrucoBetHistorySize])

        print("+++++++++++")
        print("P1 Valid truco bets")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP1"]
        print("Can bet truco:", self.stateP2[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP1"]
        print("Can bet retruco:", self.stateP2[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP1"]
        print("Can bet valecuatro:", self.stateP2[idx])

        print("P2 Valid truco bets")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoCanBetTrucoP2"]
        print("Can bet truco:", self.stateP2[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoCanBetRetrucoP2"]
        print("Can bet retruco:", self.stateP2[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["trucoCanBetValecuatroP2"]
        print("Can bet valecuatro:", self.stateP2[idx])

        print("+++++++++++")
        print("Envido Betting History")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP1"]
        print("P1:",self.stateP2[idx:idx+self.stateEnvidoBetHistorySize])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoBetHistoryP2"]
        print("P2:",self.stateP2[idx:idx+self.stateEnvidoBetHistorySize])

        print("+++++++++++")
        print("P1 Valid envido bets")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoCanBetEnvidoP1"]
        print("Can bet envido:", self.stateP2[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoCanBetRealEnvidoP1"]
        print("Can bet realenvido:", self.stateP2[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoCanBetFaltaEnvidoP1"]
        print("Can bet faltaenvido:", self.stateP2[idx])

        print("P2 Valid envido bets")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoCanBetEnvidoP2"]
        print("Can bet envido:", self.stateP2[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoCanBetRealEnvidoP2"]
        print("Can bet realenvido:", self.stateP2[idx])
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoCanBetFaltaEnvidoP2"]
        print("Can bet faltaenvido:", self.stateP2[idx])

        print("+++++++++++")
        print("Puntos publicos P1")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP1"]
        print(self.stateP2[idx:idx+22])
        print("Puntos publicos P2")
        idx = self.STATE_SECTIONS_INDECES["compartidoSection"] + self.STATE_COMPARTIDO_INDECES["envidoPuntosPublicosP2"]
        print(self.stateP2[idx:idx+22])

        print("/////////////////////////")

if __name__ == "__main__":
    game = Game(5,1)
    print(game.stateP1)
      