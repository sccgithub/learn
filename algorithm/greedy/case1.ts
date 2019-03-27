import * as scanf from 'scanf';
interface ActI {
  start: number;
  end: number;
}

let N;
let act: ActI[] = [];

const cmp = (a: ActI, b: ActI): number => a.end < b.end ? 1 : -1;

const greedy_activity_selector = () => {
  let num = 1, i = 1;
  for (let j = 2; j <= N; j++) {
    if (act[j].start >= act[i].end) {
      i++;
      num++
    }
    return num;
  }
}

const main = () => {
  console.log('input t:')
  let t = scanf('%d');
  while (t--) {
    console.log('input N:')
    N = scanf('%d');
    for (let i = 0; i < N; i++) {
      act[i] = {start: 0, end: 0};
      console.log(`input act[${i}].start:`)
      act[i].start = scanf('%d');
      console.log(`input act[${i}].end:`)
      act[i].end = scanf('%d');
    }
    act[0].start = -1;
    act[0].end = -1;
    act.sort(cmp)
    let res = greedy_activity_selector();
    console.log(res)
  }  
}

main()
