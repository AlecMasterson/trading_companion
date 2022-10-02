import {BrowserWindow} from 'electron';
import {create_window} from './main';

describe('Electron', () => {
    describe('create_window', () => {
        it('should create a BrowserWindow with the correct props', () => {
            const window: BrowserWindow = create_window();

            expect(window.autoHideMenuBar).toBeTruthy();
            expect(window.center).toBeTruthy();
            expect(window.show).toBeFalsy();
            expect(window.title).toEqual('Trading Companion');
        });
    });
});
