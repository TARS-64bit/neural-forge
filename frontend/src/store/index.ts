import { configureStore, combineReducers } from '@reduxjs/toolkit';
import { persistStore, persistReducer, FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER } from 'redux-persist';
import createWebStorage from 'redux-persist/lib/storage/createWebStorage';
import repoReducer from './repoSlice';

// Fallback for Next.js SSR so it doesn't crash when 'window' is missing
const createNoopStorage = () => {
    return {
        getItem(_key: any) { return Promise.resolve(null); },
        setItem(_key: any, value: any) { return Promise.resolve(value); },
        removeItem(_key: any) { return Promise.resolve(); },
    };
};

const storage = typeof window !== "undefined" ? createWebStorage("local") : createNoopStorage();

const persistConfig = {
    key: 'neural-forge-root',
    storage,
};

const rootReducer = combineReducers({ repo: repoReducer });
const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
    reducer: persistedReducer,
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: { ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER] },
        }),
});

export const persistor = persistStore(store);
export type AppRootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;