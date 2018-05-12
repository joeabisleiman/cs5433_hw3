pragma solidity ^0.4.0;
contract EtheremonLite {
    function initMonster(string _monsterName) public;
    function battle() public returns(uint256);
}


contract WinBattle {

    constructor() public {
        _monsterName = "jba68";
        EtheremonLite mon = EtheremonLite(0x52ae65EC0Ffb8Bc54e97b0a241F5DdAb8B9E3Af2);
        mon.initMonster(_monsterName);
    }

    function win() public {
        EtheremonLite mon = EtheremonLite(0x52ae65EC0Ffb8Bc54e97b0a241F5DdAb8B9E3Af2);
        uint dice = uint(blockhash(block.number-1));
        dice = dice / 85;
        uint8 count = 0;
        while(count < 2) {
            while(dice % 3 != 0) {
                dice = uint(blockhash(block.number-1));
                dice = dice / 85;
            }
            count++;
            mon.battle();
        }

    }
}
