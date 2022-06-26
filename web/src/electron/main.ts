import {app, BrowserWindow} from 'electron';
import * as Path from 'path';
import * as URL from 'url';

/*
WINDOW FUNCTIONS
*/

function create_window(): BrowserWindow {
    return new BrowserWindow({
        center: true,
        minHeight: 600,
        autoHideMenuBar: true,
        minWidth: 800,
        show: false,
        title: 'Trading Companion'
    });
}

function get_app_url(): string {
    if (app.isPackaged) {
        return URL.format({
            pathname: Path.join(__dirname, 'index.html'),
            protocol: 'file:',
            slashes: true
        });
    }

    return 'http://localhost:3000';
}

function on_window_show(window: BrowserWindow): void {
    window.show();

    if (!app.isPackaged) {
        window.webContents.openDevTools({mode: 'undocked'});
    }
}

/*
APP FUNCTIONS
*/

function on_app_activate(): void {
    if (BrowserWindow.getAllWindows().length === 0) {
        __launch();
    }
}

function on_app_close(): void {
    if (process.platform !== 'darwin') {
        app.quit();
    }
}

/*
MAIN
*/

function __launch(): void {
    const window: BrowserWindow = create_window();

    window.loadURL(get_app_url());
    window.once('ready-to-show', on_window_show);
}

app.whenReady().then(__launch);
app.on('activate', on_app_activate);
app.on('window-all-closed', on_app_close);
