import { createStore } from "redux";

const store = createStore(reducer);

function Reducer(state, action) {
    switch(action.type) {
        case "PENDING_FILTER": return { value: action.value_1 };
        case "ALL_AVAILABLE": return { value: action.value_2 };
        
        default: return state;
    }
}

export default store;