import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface RepoState {
    githubUrl: string;
    githubPat: string;
    githubBranch: string;
    repoOwner: string;
    repoName: string;
    maxLoops: number;
}

const initialState: RepoState = {
    githubUrl: "",
    githubPat: "",
    githubBranch: "main",
    repoOwner: "",
    repoName: "",
    maxLoops: 3
};

const repoSlice = createSlice({
    name: 'repo',
    initialState,
    reducers: {
        setRepoDetails: (state, action: PayloadAction<RepoState>) => {
            return { ...state, ...action.payload };
        },
        clearRepoDetails: () => initialState,
    },
});

export const { setRepoDetails, clearRepoDetails } = repoSlice.actions;
export default repoSlice.reducer;