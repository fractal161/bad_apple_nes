prgBankAddr = 0x0A
prgVideoDataPtrAddr = 0x0B
chrBankAddr = 0x0D
chrVideoDataPtrAddr = 0x0E
apuBankAddr = 0x6597
apuPtrAddr = 0x7D

function readByte(addr, memType)
	memType = memType or emu.memType.cpuDebug
	return emu.read(addr, memType)
end

function readWord(addr, memType)
	memType = memType or emu.memType.cpuDebug
	return emu.readWord(addr, memType)
end

function draw()
	local chrString = string.format("CHR PTR: %04X [%02X]",
									readWord(chrVideoDataPtrAddr),
									readByte(chrBankAddr))
	local prgString = string.format("PRG PTR: %04X [%02X]",
									readWord(prgVideoDataPtrAddr),
									readByte(prgBankAddr))
	emu.drawString(0, 0, chrString, 0xFFFFFF, 0x000000)
	emu.drawString(0, 8, prgString, 0xFFFFFF, 0x000000)
	local apuLabels = {"SQ1", "SQ2", "TRI", "NOI"}
	local x = {0, 0, 2, 1}
	for i=1,4 do
		local channelPtrAddr = apuPtrAddr+2*i-2
		local channelBankAddr = apuBankAddr+2*i-2
		local channelString = string.format("%s PTR: %04X [%02X]",
									apuLabels[i],
									readWord(channelPtrAddr),
									readByte(channelBankAddr))
		emu.drawRectangle(0, 8*(i+1), 8, 8, 0x000000, true)
		emu.drawString(x[i], 8*(i+1), channelString, 0xFFFFFF, 0x000000)
	end
end

emu.addEventCallback(draw, emu.eventType.startFrame)
-- emu.registerMemoryCallback()
