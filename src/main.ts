src/test-issue-76.test.ts
import { describe, expect, it } from 'jest-dom';
import * as assertMock from './assert_mock.rs';

describe('Test Issue 76 - Infinite Monad Generator', () => {
    let monads: Promise<unknown>[] = []; // Stack of promises to resolve
    
    beforeAll(() => {
        console.log('[INIT] Loading infinite monad generator...');
        
        const mockPromiseStack = new Array(10); // Initial stack size
        
        for (let i = 0; i < 30; i++) {
            let p: Promise<unknown> = await Promise.race([
                setTimeout(() => console.log(`[INIT] Resolving promise ${i}`), 
                async () => new Promise((resolve) => mockPromiseStack.push(resolve)), // Simulate random errors to fill stack
                resolve('success')
            ]);

            if (p !== 'success' && p instanceof Error) {
                throw p;
            } else if (!mockPromiseStack.includes(p)) {
                console.log(`[INIT] Resolving promise ${i} successfully`);
                mockPromiseStack.push(p); // Add to stack as it resolves
            }
        }

        await Promise.all(mockPromiseStack.map((p) => p)); // Resolve all promises from the initial list
    });

    afterAll(() => {
        console.log('[FINISH] Infinite monad generator finished.');
        
        assertMock.assert('Test Issue 76 - Monads stack is valid');
    });
});
