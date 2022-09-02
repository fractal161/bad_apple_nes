prgBankAddr = 0x0A
prgVideoDataPtrAddr = 0x0B
chrBankAddr = 0x0D
chrVideoDataPtrAddr = 0x0E
apuBankAddr = 0x6597
apuPtrAddr = 0x7D
patchStartPtrAddr = 0x40
patchEndPtrAddr = 0x41
dmcConflictAddr = 0x42

function readByte(addr, memType)
	memType = memType or emu.memType.cpuDebug
	return emu.read(addr, memType)
end

function readWord(addr, memType)
	memType = memType or emu.memType.cpuDebug
	return emu.readWord(addr, memType)
end

minLength = 257
lastPatchStart = 0
lastPatchEnd = 0

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

	local patchStart = readByte(patchStartPtrAddr)
	local patchEnd = readByte(patchEndPtrAddr)
	local startDiff = (patchStart - lastPatchStart) % 256
	local endDiff = (patchEnd - lastPatchEnd) % 256
	emu.drawString(0, 8*6, string.format("BUF STT: %04X (+%02X)", 0x6400+patchStart, startDiff), 0xFFFFFF, 0x000000)
	emu.drawString(0, 8*7, string.format("BUF END: %04X (+%02X)", 0x6400+patchEnd, endDiff), 0xFFFFFF, 0x000000)
	lastPatchStart = patchStart
	lastPatchEnd = patchEnd

	local length = (patchEnd-patchStart) % 256 + 1
	if length == 1 then length = 257 end
	minLength = math.min(minLength, length)
	emu.drawString(0, 8*8, string.format("CUR LEN: %02X", length), 0xFFFFFF, 0x000000)
	emu.drawString(0, 8*9, string.format("MIN LEN: %02X", minLength), 0xFFFFFF, 0x000000)
	if readByte(dmcConflictAddr) > 0 then
		emu.drawRectangle(0,0,256,240, 0xC0FF0000, true)
	end
end

emu.addEventCallback(draw, emu.eventType.startFrame)
-- emu.registerMemoryCallback()
