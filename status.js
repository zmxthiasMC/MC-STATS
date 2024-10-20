const axios = require('axios');
const chalk = require('chalk');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function printStatusLogo() {
    const logo = `
${chalk.greenBright('░██████╗████████╗░█████╗░████████╗██╗░░░██╗░██████╗')}
${chalk.greenBright('██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║░░░██║██╔════╝')}
${chalk.greenBright('╚█████╗░░░░██║░░░███████║░░░██║░░░██║░░░██║╚█████╗░')}
${chalk.greenBright('░╚═══██╗░░░██║░░░██╔══██║░░░██║░░░██║░░░██║░╚═══██╗')}
${chalk.greenBright('██████╔╝░░░██║░░░██║░░██║░░░██║░░░╚██████╔╝██████╔╝')}
${chalk.greenBright('╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░░╚═════╝░╚═════╝░')}
    `;
    console.log(logo);
}

async function getServerInfo(ip, port, edition) {
    if (edition.toLowerCase() === 'java') {
        return await getJavaServerInfo(ip, port);
    } else if (edition.toLowerCase() === 'bedrock') {
        return await getBedrockServerInfo(ip, port);
    } else {
        return { error: 'Edición no soportada. Usa "Java" o "Bedrock".' };
    }
}

async function getJavaServerInfo(ip, port) {
    try {
        const response = await axios.get(`https://api.mcsrvstat.us/2/${ip}:${port}`);
        const data = response.data;
        return {
            IP: ip,
            Port: port,
            MOTD: data.motd.clean.join(' '),
            Players: data.players.online,
            MaxPlayers: data.players.max,
            Edition: 'Java',
            Host: data.hostname,
            Protocol: data.protocol,
            Plugins: data.plugins ? data.plugins.names : [],
            Online: data.online,
            Version: data.version,
            Software: data.software,
            Ping: data.debug.ping,
            Worlds: data.worlds,
            Lobby: data.lobby,
            ProtocolVersion: data.protocol_version,
            ServerType: data.server_type,
            Uptime: data.uptime,
            PlayerIPs: data.players.sample ? data.players.sample.map(player => player.name) : [],
            ServerDescription: data.description,
            Map: data.map,
            GameMode: data.gamemode,
            Difficulty: data.difficulty,
            Whitelist: data.whitelist,
            BannedPlayers: data.banned_players,
            Operators: data.operators
        };
    } catch (error) {
        return { error: error.message };
    }
}

async function getBedrockServerInfo(ip, port) {
    try {
        const response = await axios.get(`https://api.mcsrvstat.us/2/${ip}:${port}`);
        const data = response.data;
        return {
            IP: ip,
            Port: port,
            MOTD: data.motd.clean.join(' '),
            Players: data.players.online,
            MaxPlayers: data.players.max,
            Edition: 'Bedrock',
            Host: data.hostname,
            Protocol: data.protocol,
            Plugins: data.plugins ? data.plugins.names : [],
            Online: data.online,
            Version: data.version,
            Software: data.software,
            Ping: data.debug.ping,
            Worlds: data.worlds,
            Lobby: data.lobby,
            ProtocolVersion: data.protocol_version,
            ServerType: data.server_type,
            Uptime: data.uptime,
            PlayerIPs: data.players.sample ? data.players.sample.map(player => player.name) : [],
            ServerDescription: data.description,
            Map: data.map,
            GameMode: data.gamemode,
            Difficulty: data.difficulty,
            Whitelist: data.whitelist,
            BannedPlayers: data.banned_players,
            Operators: data.operators
        };
    } catch (error) {
        return { error: error.message };
    }
}

async function main() {
    printStatusLogo();

    rl.question('IP del servidor: ', (ip) => {
        rl.question('Puerto del servidor: ', (port) => {
            rl.question('¿Java o Bedrock?: ', async (edition) => {
                const serverInfo = await getServerInfo(ip, port, edition);

                if (serverInfo.error) {
                    console.log(chalk.red(serverInfo.error));
                } else {
                    console.log(chalk.greenBright(JSON.stringify(serverInfo, null, 4)));
                }

                rl.close();
            });
        });
    });
}

main();
          
