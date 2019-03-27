// 假设1元、2元、5元、10元、20元、50元、100元的纸币
// 分别有c0, c1, c2, c3, c4, c5, c6张。
// 现在要用这些钱来支付K元，至少要用多少张纸币？
// 用贪心算法的思想，很显然，每一步尽可能用面值大的纸币即可。
// 在日常生活中我们自然而然也是这么做的。在程序中已经事先将Value按照从小到大的顺序排好


import * as scanf from 'scanf';

const count = [3, 0, 2, 1, 0, 3, 5];
const value = [1, 2, 5, 10, 20, 50, 100];

const solve = (money: number): number => {
  let num = 0;
  for (let i = value.length - 1; i >= 0 ; i--) {
    let c = Math.min(Math.floor(money / value[i]), count[i]);
    console.log(c);
    console.log(money);
    
    money = money - c * count[i];
    num += c;
  }
  if (money > 0) {
    num = -1;
  }
  return num;
}

const main = (): void => {
  console.log('input maney:')
  let money = scanf('%d');
  let res = solve(money);
  console.log(res == -1 ? 'NO' : res);
}

main();